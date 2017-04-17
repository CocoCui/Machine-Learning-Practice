import sys
import numpy as np
from pyspark import SparkContext
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
div = 13
div2 = 80
def parseInfo(line):
    a = line.split("\t")
    songname = a[0]
    songvec = a[1].split(" ")
    veclist = []
    i = 1
    while i < len(songvec):
        vec = []
        for idx in range(0,div):
            vec.append(float(songvec[i].replace("\n","")))
            i += 1
        veclist.append(vec)
    return (songname,veclist)

def parseSignal(line):
    a = line.split("\t")
    rate = int(a[0])
    sig = []
    sigs = a[1].split(" ")
    for i in range(0,len(sigs)-1):
        sig.append(int(sigs[i]))
    return (rate,sig)

def vecdis(veclist1,veclist2):
    dis = 0
    for i in range(0,len(veclist1)):
        for j in range(0,len(veclist1[i])):
            dis += (veclist1[i][j] - veclist2[i][j])**2
    return dis

def caldis(songvec,mfcclist):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    songname = songvec[0]
    vec = songvec[1]
    mindis = float("+inf")
    minidx0 = -1
    minidx1 = -1
    for i in range(0, div2, 4):
        for startidx in range(0,len(vec) - len(mfcclist[i])):
            dis = vecdis(mfcclist[i],vec[startidx : len(mfcclist[i])+startidx])
            if dis < mindis:
                mindis = dis
                minidx0 = minidx1
                minidx1 = i
    for off in range(-3,4):
        i = minidx0 + off
        if i < 0 or i > div2 or i % 4 == 0:
            continue
        for startidx in range(0,len(vec) - len(mfcclist[i])):
            dis = vecdis(mfcclist[i],vec[startidx : len(mfcclist[i])+startidx])
            if dis < mindis:
                mindis = dis
    for off in range(-3,4):
        i = minidx1 + off
        if i < 0 or i > div2 or i % 4 == 0:
            continue
        for startidx in range(0,len(vec) - len(mfcclist[i])):
            dis = vecdis(mfcclist[i],vec[startidx : len(mfcclist[i])+startidx])
            if dis < mindis:
                mindis = dis
    return  (songname,mindis)

def filterfunc(ele,fset):
    if ele in fset:
        return True
    return False

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sc = SparkContext(appName="MusicSearch")
    lines = sc.textFile("hdfs://192.168.1.106:9000/mfcc.txt")
    songs = lines.map(parseInfo).cache()
    lines2 = sc.textFile("hdfs://192.168.1.106:9000/input.txt")
    signal = lines2.map(parseSignal).collect()[0]
    rate = int(signal[0])
    sig_org = np.array(signal[1])
    mfcclist = []
    mfcclist_pre = []
    for i in range(0,div2):
        start = int(rate/float(div2) * i)
        sig = sig_org[start+rate:start+rate*6]
        mfcc_feat = mfcc(sig,rate,winlen=1,winstep=1)
        mfcclist_pre.append(mfcc_feat)
        sig = sig_org[start:]
        mfcc_feat = mfcc(sig,rate,winlen=1,winstep=1)
        mfcclist.append(mfcc_feat)
    #print signal[1]
    dis = songs.map(lambda s:caldis(s,mfcclist_pre)).collect()
    dis.sort(lambda x,y:cmp(x[1],y[1])) 
    filterlist = set()
    for i in range(0,100):
        filterlist.add(dis[i][0])
    songs = songs.filter(lambda s:filterfunc(s[0],filterlist))
    dis = songs.map(lambda s:caldis(s,mfcclist)).collect()
    dis.sort(lambda x,y:cmp(x[1],y[1]))
    for i in range(0,10):
        print dis[i][0]

