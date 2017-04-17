import sys
import numpy as np
from pyspark import SparkContext

def parseInfo(line):
    parts = line.split(" ");
    movieID = int(parts[0])
    idx = 1
    dic = []
    while idx < len(parts) - 1:
        dic.append((int(parts[idx]),1.0))
        idx += 1
    return movieID, dic
    
def calDis(v1,v2):
    dic = {};
    for e in v1:
        dic[e[0]] = e[1]
    for e in v2:
        if e[0] in dic:
            dic[e[0]] = dic[e[0]] - e[1]
        else:
            dic[e[0]] = e[1]
    dis = 0.0
    for e in dic:
        if e < 10000:
            dis += dic[e]**2
        else:
            dis += (dic[e]**2)*5
    return dis

def closestPoint(p, centers):
    bestIndex = 0
    closest = float("+inf")
    for i in range(len(centers)):
        tempDist = calDis(p[1],centers[i][1])
        if tempDist < closest:
            closest = tempDist
            bestIndex = i
    return bestIndex

def calCenter(id,veclist):
    dic = {};
    print "Cluster ID",id,"Size",len(veclist)
    for ele in veclist:
        for e in ele[1]:
            if e[0] in dic:
                dic[e[0]] = dic[e[0]] + e[1]
            else:
                dic[e[0]] = e[1]
    res = []
    count = len(veclist)
    for e in dic:
        res.append((e,float(dic[e])/count))
    return (0,res)
    
if __name__ == "__main__":
    sc = SparkContext(appName="PythonKMeans")
    lines = sc.textFile("data/outfile")
    data = lines.map(parseInfo).cache()
    K = 500;
    kPoints = data.takeSample(False, K, 1)
    for i in range(0,1):
        closest = data.map( lambda p : (closestPoint(p,kPoints), p)).cache()
        centers = closest.groupByKey()
        newCenters = centers.map(lambda p : (p[0],calCenter(p[0],p[1]))).collect()
        for (iK,p) in newCenters:
            kPoints[iK] = p
    out0 = closest.map(lambda p : (p[1][0],p[0])).collect()
    for (clusterid, id) in out0:
        print clusterid, id
