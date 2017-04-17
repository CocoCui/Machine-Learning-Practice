import re
import os
import math
import random
from sklearn import svm
from sklearn import preprocessing
from sklearn import tree
from nltk import SnowballStemmer

testfilename = "testset_txt_img_cat.list"
trainfilename = "trainset_txt_img_cat.list"
textpre = "texts/"
testset = []
trainset = {}
vocabulary  = []
vocabulary_vector  = []
vp = {}
P = {}
trainsize = 0
wordlen = 4
train_vec = []
test_vec = []
train_res = []
test_res = []
idf = {}
stemmer = SnowballStemmer("english")
alltest = []
vote = []

def gettraindata():
    global trainsize
    global vocabulary
    for i in range(1, 11):
        ll = []
        trainset[i] = ll
        
    for line in open(trainfilename):
        trainsize += 1
        v = line.strip().split()
        textfile = textpre + v[0] + ".xml"
        imgfilefile = v[1]
        category = int(v[2])
        v = open(textfile)
        text = v.read()
        hh = v.read()
        text = re.search("<text>([\w\W]*)</text>",text).group(1)
        words = re.findall("\W([\w]+)\W",text)
        words2 = []
        for word in words:
            #word = stemmer.stem(word)
            if len(word) >= wordlen:
                word = word.lower()
                vocabulary.append(word)
                words2.append(word)
        txt = {}
        txt["words"] = words2
        txt["category"] = category
        alltest.append(txt)
        trainset[category].append(txt)
    vocabulary = list(set(vocabulary))


def gettestdata():
    global vocabulary
    for line in open(testfilename):
        v = line.strip().split()
        textfile = textpre + v[0] + ".xml"
        imgfilefile = v[1]
        category = int(v[2])
        v = open(textfile)
        text = v.read()
        text = re.search("<text>([\w\W]*)</text>",text).group(1)
        words = re.findall("\W([\w]+)\W",text)
        words2 = []
        for word in words:
            #word = stemmer.stem(word)
            if len(word) >= wordlen:
                word = word.lower()
                words2.append(word)
        txt = {}
        txt["words"] = words2
        txt["category"] = category
        testset.append(txt)

def train():
    global vocabulary
    for i in range(1, 11):
        Text = [];
        P[i] = float(len(trainset[i])) / trainsize;
        for txt in trainset[i]:
            for word in txt["words"]:
                Text.append(word)
        n = len(Text)
        pwi = {};
        vp[i] = pwi;
        for word in vocabulary:
            pwi[word] = 0.0;
        for word in Text:
            if word in pwi:
                pwi[word] += 1;
        for word in pwi:
            pwi[word] = (pwi[word] + 1) / (n + len(vocabulary)) * 10000 

def vote_nb():
    right = 0
    vset = set(vocabulary)
    right = 0.0
    if len(vote) == 0:
        for i in range(0,len(testset)):
            vv = {}
            for i in range(1,11):
                vv[i] = 0;
            vote.append(vv)
    for idx in range(0,len(testset)):
        test = testset[idx]
        cat = 0
        maxp = -1
        pp = [];
        for i in range(1,12):
            pp.append(1.0);
        for i in range(1,11):
            pp[i] *= P[i]
            for w in test["words"]:
                if w in vset: 
                    pp[i] *= vp[i][w];
                    if(pp[i] > 100000):
                        for j in range(1, 11):
                            pp[j] /= 100000;
        for i in range(1,11):
            if pp[i] > maxp:
                cat = i;
                maxp = pp[i];
        if cat == test["category"]:
            right += 1;
        vote[idx][cat] += 1
    print "Accuracy :", (right / len(testset)) 
def predict():
    right = 0.0
    for idx in range(0,len(testset)):
        test = testset[idx]
        cat = 0
        maxvote = -1
        for i in range(1,11):
            if maxvote < vote[idx][i]:
                cat = i
                maxvote = vote[idx][i]
        if cat == test["category"]:
            right += 1;
    print right / len(testset)

def rand_trainset():
    global vocabulary
    vocabulary = []
    totsize = len(alltest)
    for i in range(1, 11):
        ll = []
        trainset[i] = ll
    for i in range(0,totsize):
        idx = random.randint(0, totsize -1);
        txt = alltest[idx]
        for word in txt["words"]:
            vocabulary.append(word)
        cat = txt["category"]
        trainset[cat].append(txt)
    vocabulary = list(set(vocabulary))

if __name__ == "__main__":
    gettraindata()
    print "traindata get"
    gettestdata()
    print "testdata get"
    for i in range(0, 100):
        rand_trainset()
        print "Round",i
        train()
        vote_nb()
    print "total accuracy"
    predict()
    #x2test()
    #print "word choosed"
    #vocabulary_vector = vocabulary
    #traindata_vector()
    #print "train vector generated"
    #testdata_vector()
    #print "test vector generated"
    #test_svm()
    
