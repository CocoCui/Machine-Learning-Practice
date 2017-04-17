import re
import os
import math
import numpy as np
import cv2
from sklearn import svm
from sklearn import preprocessing
from sklearn import tree

testfilename = "testset_txt_img_cat.list"
trainfilename = "trainset_txt_img_cat.list"
imgpre = "images/"
test_imgset = []
train_imgset = []
test_vec = []
test_res = []
train_vec = []
train_res =[]
cat_count = {}
def gettraindata():
    id = 0;
    for i in range(1,11):
        cat_count[i] = 0.0
    for line in open(trainfilename):
        print id
        id += 1
        v = line.strip().split()
        imgfilefile = imgpre + v[1] + ".jpg"
        category = int(v[2])
        img = cv2.imread(imgfilefile)
        imginfo = {}
        imginfo["image"] = img
        h = float(img.shape[0])
        w = float(img.shape[1])
        b,g,r = cv2.split(img)
        hb = cv2.calcHist([b],[0],None,[256],[0.0,255.0])
        hg = cv2.calcHist([g],[0],None,[256],[0.0,255.0])
        hr = cv2.calcHist([r],[0],None,[256],[0.0,255.0])
        his = []
        for i in hb:
            his.append(float(i)/(h*w))
        for i in hg:
            his.append(float(i)/(h*w))
        for i in hr:
            his.append(float(i)/(h*w))
        imginfo["category"] = category
        cat_count[category] += 1
        imginfo["his"] = his
        train_imgset.append(imginfo)
        train_vec.append(his)
        train_res.append(category)

def gettestdata():
    id = 0;
    for line in open(testfilename):
        print id
        id += 1
        if id > 100:
            break
        v = line.strip().split()
        imgfilefile = imgpre + v[1] + ".jpg"
        category = int(v[2])
        img = cv2.imread(imgfilefile)
        imginfo = {}
        imginfo["image"] = img
        h = float(img.shape[0])
        w = float(img.shape[1])
        b,g,r = cv2.split(img)
        hb = cv2.calcHist([b],[0],None,[256],[0.0,255.0])
        hg = cv2.calcHist([g],[0],None,[256],[0.0,255.0])
        hr = cv2.calcHist([r],[0],None,[256],[0.0,255.0])
        his = []
        for i in hb:
            his.append(float(i)/(h*w))
        for i in hg:
            his.append(float(i)/(h*w))
        for i in hr:
            his.append(float(i)/(h*w))
        imginfo["category"] = category
        imginfo["his"] = his
        test_imgset.append(imginfo)
        test_vec.append(his)
        test_res.append(category)

def svm_test():
    clf = svm.SVC();
    clf.fit(train_vec,train_res)
    idx = 0;
    right = 0.0
    for v in test_vec:
        res = test_res[idx];
        if clf.predict(v) == res:
            right += 1
        idx += 1
    print "SVM:"
    print right / len(test_vec)

def cal_dis(his1, his2):
    dis = 0.0 
    for i in range(0,len(his1)):
        dis += (his1[i] - his2[i])**2
    return dis;

def predict_by_his():
    weight = {}
    right = 0.0
    predict = 0.0
    for i in range(1,11):
        weight[i] = cat_count[i] / len(train_vec)
        weight[i] = (1.0 / weight[i]) / 10.0
    for i in range(0,50):
        v = test_vec[i]
        res = []
        vote = []
        for j in range(0,11):
            vote.append(0.0)
        for vv in train_imgset:
            dis = cal_dis(v,vv["his"])
            cat = vv["category"]
            e = []
            e.append(cat)
            e.append(dis)
            e.append(vv["image"])
            res.append(e)
        res.sort(key = lambda x:x[1])
        cv2.namedWindow("Image")   
        cv2.imshow("Image", test_imgset[i]["image"])
        print "test IMG"
        raw_input()
        for j in range(0,3):
            cv2.namedWindow("Image")   
            cv2.imshow("Image", res[j][2])
            raw_input()
        for j in range(0,20):
            vote[res[j][0]] += 1
        max = -1;
        cat = 0;
        for j in range(1,11):
            if vote[j] > max:
                max = vote[j]
                cat = j
        if max > 4:
            predict += 1;
            if cat == test_res[i]:
                right += 1;
    print right,predict

if __name__ == "__main__":
    gettestdata()
    print "testdata get"
    gettraindata()
    print "traindata get"
    predict_by_his()
