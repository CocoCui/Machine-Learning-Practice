import re
import os
import math
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
            word = stemmer.stem(word)
            if len(word) >= wordlen:
                word = word.lower()
                vocabulary.append(word)
                words2.append(word)
        txt = {}
        txt["words"] = words2
        trainset[category].append(txt)
    vocabulary = list(set(vocabulary))


def gettestdata():
    global vocabulary
    vset = set(vocabulary)
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
            word = stemmer.stem(word)
            if len(word) >= wordlen and (word in vset):
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

def predict():
    right = 0
    for test in testset:
        cat = 0
        maxp = -1
        pp = [];
        for i in range(1,12):
            pp.append(1.0);
        for i in range(1,11):
            pp[i] *= P[i]
            for w in test["words"]:
                pp[i] *= vp[i][w];
                if(pp[i] > 100000):
                    for j in range(1, 11):
                        pp[j] /= 100000;
        for i in range(1,11):
            if pp[i] > maxp:
                cat = i;
                maxp = pp[i];
        if test["category"] == cat:
            right += 1;
    print "Naive Bayesian:"
    print float(right)/len(testset) 

def x2test():
    global vocabulary
    global vocabulary_vector
    vs = set(vocabulary)
    wd = {}
    for i in range(1,11):
        wl = {}
        wd[i] = wl
        for word in vocabulary:
            abcd = {}
            abcd["A"] = 0
            abcd["B"] = 0
            abcd["C"] = 0
            abcd["D"] = 0
            wl[word] = abcd;
    for i in range(1,11):
        for txt in trainset[i]:
            cat = i
            wordset = set(txt["words"])
            for word in wordset:
                if word in vs:
                    wd[cat][word]["A"] += 1.0;
                    for j in range(1,11):
                        if j == cat:
                            continue;
                        wd[j][word]["B"] += 1.0
        for word in vocabulary:
            wd[cat][word]["C"] = len(trainset[cat]) - wd[cat][word]["A"];
    for i in range(1,11):
        for word in vocabulary:
            wd[i][word]["D"] = trainsize - len(trainset[i]) - wd[i][word]["B"];
    for i in range(1,11):
        word_value = {};
        for word in vocabulary:
            word_value[word] = wd[i][word]["A"]*wd[i][word]["D"] - wd[i][word]["B"]*wd[i][word]["C"]
            word_value[word] /= (wd[i][word]["A"]+wd[i][word]["C"])
            word_value[word] /= (wd[i][word]["A"]+wd[i][word]["B"])
            word_value[word] /= (wd[i][word]["B"]+wd[i][word]["D"])
            if wd[i][word]["C"]+wd[i][word]["D"] == 0:
                word_value[word] = 0.0
            else:
                word_value[word] /= (wd[i][word]["C"]+wd[i][word]["D"])
            word_value[word] *= trainsize
        word_value = sorted(word_value.iteritems(), key = lambda word_value:word_value[1], reverse = True)
        for j in range(1, 3000):
            vocabulary_vector.append(word_value[j][0]);
        
def testdata_vector():
    global vocabulary_vector
    vs = set(vocabulary_vector)
    for test in testset:
        vector = {}
        vec = []
        for word in vocabulary_vector:
            vector[word] = 0.0;
        for word in test["words"]:
            if word in vs:
                vector[word] += 1.0
        for word in vocabulary_vector:
            if vector[word] != 0:
                    vector[word] = vector[word] / len(test["words"]);
                    vector[word] = vector[word] * idf[word]
            vec.append(vector[word])
        test_vec.append(vec)
        test_res.append(test["category"])

def traindata_vector():
    global vocabulary_vector,idf
    vs = set(vocabulary_vector)
    for word in vocabulary_vector:
        idf[word] =1.0;
    for i in range(1,11):
        for txt in trainset[i]:
            for word in set(txt["words"]):
                if word in vs:
                    idf[word] += 1.0;
    for word in vocabulary_vector:
        idf[word] = math.log(trainsize / idf[word],2);
    for i in range(1,11):
        for txt in trainset[i]:
            train_res.append(i)
            vector = {}
            vec = []
            for word in vocabulary_vector:
                vector[word] = 0;
            for word in txt["words"]:
                if word in vs:
                    vector[word] += 1.0
            for word in vocabulary_vector:
                if vector[word] != 0:
                    vector[word] = vector[word] / len(txt["words"]);
                    vector[word] = vector[word] * idf[word]    
                vec.append(vector[word])
            train_vec.append(vec)

def test_svm():
    global train_vec,test_vec
    clf = svm.SVC(kernel='linear');
    scaler = preprocessing.MinMaxScaler()
    train_vec = scaler.fit_transform(train_vec)
    test_vec = scaler.fit_transform(test_vec)
    clf.fit(train_vec, train_res)
    idx = 0;
    right = 0.0
    for v in test_vec:
        res = test_res[idx];
        if clf.predict(v) == res:
            right += 1
        idx += 1
    print "SVM:"
    print right / len(test_vec)

def test_tree():
    global train_vec,test_vec
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(train_vec, train_res)
    idx = 0;
    right = 0.0
    for v in test_vec:
        res = test_res[idx];
        if clf.predict(v) == res:
            right += 1
        idx += 1
        print idx
    print "Decision:"
    print right / len(test_vec)

if __name__ == "__main__":
    gettraindata()
    print "traindata get"
    train()
    print "train finished"
    gettestdata()
    print "testdata get"
    predict()
    #x2test()
    #print "word choosed"
    #vocabulary_vector = vocabulary
    #traindata_vector()
    #print "train vector generated"
    #testdata_vector()
    #print "test vector generated"
    #test_svm()
    
