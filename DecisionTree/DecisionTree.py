#python version: 3.5.2
import pandas as pd
import numpy as np
from sklearn import tree
from math import log2
import pydotplus
from collections import deque
import random
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter

def entropy1(data):
    tot = sum(data)
    en = 1.0
    for i in data:
        if i > 0:
            en = en - (i / tot) * log2((i / tot))
    return en

def entropy2(left, right):
    l = left.values()
    r = right.values()
    tot = sum(l) + sum(r)
    le, re = entropy1(l), entropy1(r)
    en = le * sum(l) / tot + re * sum(r) / tot
    return en

class Node:
    classTag = None
    leaf = 0
    attribute = None
    split = None
    left = None
    right = None
    entropy = 0
    def __init__(self, X, y, depth, max_depth, data, parentClass):
        self.classTag, count, self.entropy = self.findMajority(y, data, parentClass)
        if count == len(data) or depth == max_depth:
            self.leaf = 1
            return
        sub_y = y[data]
        maxGain, splitAttribute = 0, 0
        for attribute in X.columns.values:
            gain, split = self.informationGain(attribute, data, X, y, self.entropy)
            if maxGain < gain:
                maxGain = gain
                self.attribute = attribute
                self.split = split
        if maxGain == 0:
            self.leaf = 1
            return
        leftData = []
        rightData = []
        for i in data:
            if X[self.attribute][i] < self.split:
                leftData.append(i)
            else:
                rightData.append(i)
        self.left = Node(X, y, depth + 1, max_depth, leftData, self.classTag)
        self.right = Node(X, y, depth + 1, max_depth, rightData, self.classTag)
        return

    def printNode(self):
        print("Entropy:" + str(self.entropy))
        print(self.count)
        if self.leaf:
            print("Leaf Node, class:" + str(self.classTag))
        else:
            print("Inner Node, column: " + str(self.attribute) + " <= " + str(self.split) + "?")
        print("--------------------------------------------")
    
            
    def informationGain(self, attribute, data, X, y, curEntropy):
        #find the best split first
        sub_x = X[attribute][data].sort_values(inplace = False)
        sub_y = y[data]
        count_right, count_left  = Counter(sub_y), {}
        for c in count_right:
            count_left[c] = 0.0
        minEntropy = curEntropy + 1
        split = 0
        same = 0
        values = list(sub_x)
        for i in range(0, len(data) - 1):
            index = sub_x.index[i]
            count_left[y[index]] += 1
            count_right[y[index]] -= 1
            if not np.isnan(values[i]) and not np.isnan(values[i + 1]) and values[i] != values[i+1]:
                en = entropy2(count_left, count_right)
                same = 0
                if en < minEntropy:
                    split = (values[i] + values[i+1]) / 2
                    minEntropy = en
        return (curEntropy - minEntropy), split
            
                
            
    def findMajority(self, y, data, parentClass):
        count = Counter(y[data])
        self.count = count
        curEntropy = entropy1(count)
        major, maxCount = parentClass, 0
        for i in count:
            if count[i] > maxCount:
                major = i
                maxCount = count[i]
        return major, maxCount, curEntropy

    

class DecisionTree:
    root = None
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.root = Node(X, y, 0, self.max_depth, [i for i in range(len(y))], 0)
    
    def predict(self, T):
        result = []
        for index, row in T.iterrows():
            node = self.root
            while not node.leaf:
                if row[node.attribute] < node.split:
                    node = node.left
                else:
                    node = node.right
            result.append(node.classTag)
        return result


    def print(self):
        que = deque()
        que.appendleft(self.root)
        while len(que):
            node = que.popleft()
            if node == None:
                continue
            else:
                node.printNode()
                que.append(node.left)
                que.append(node.right)

def validation_curve():
    dataFile = open("arrhythmia.csv")
    x, y = [], []
    attr_value = [[] for i in range(280)]
    for line in dataFile.readlines():
        attributes = line.strip("\n").split(",")
        for i in range(len(attributes)):
            if attributes[i] == "?":
                attributes[i] = np.nan
            else:
                attributes[i] = np.float64(attributes[i])
                attr_value[i].append(np.float64(attributes[i]))
        classTag = int(attributes[-1])
        attributes = attributes[:len(attributes) - 1]
        x.append(attributes)
        y.append(classTag)
    
    for i in range(280):
        attr_value[i] = Counter(attr_value[i]).most_common(1)
    for row in x:
        for i in range(len(row)):
            if np.isnan(row[i]):
                row[i] = attr_value[i][0][0]

    dataSize = len(x)
    dataList = [i for i in range(dataSize)]
    random.shuffle(dataList)
    part_x, part_y = [], []
    
    for i in range(3):
        tmp_x = []
        tmp_y = []
        for j in range(int(i * dataSize / 3), int((i + 1) * dataSize / 3)):
            tmp_x.append(x[dataList[j]])
            tmp_y.append(y[dataList[j]])
        part_x.append(tmp_x)
        part_y.append(tmp_y)
    part = []
    part_list = []
    for i in range(3):
        train_x, train_y = [],[]
        test_x, test_y = [], []
        for j in range(3):
            if j == i:
                test_x.extend(part_x[i])
                test_y.extend(part_y[i])
            else:
                train_x.extend(part_x[j])
                train_y.extend(part_y[j])
        X, Y = pd.DataFrame.from_dict(train_x), pd.Series(train_y)
        x, y = pd.DataFrame.from_dict(test_x), pd.Series(test_y)
        part.append({"train": (X,Y), "test": (x, y)})
        part_list.append({"train": (train_x, train_y), "test": (test_x, test_y)})
    accRate = {"train":[], "test":[]}
    depths = []
    for depth in range(2,20,2):
        depths.append(depth)
        acc_test = []
        acc_train = []
        print("Depth:" + str(depth))
        for r in range(3):
            print("Round " + str(r))
            t = DecisionTree(depth)
            t.fit(part[r]["train"][0], part[r]["train"][1])
            res = t.predict(part[r]["test"][0])
            y = part[r]["test"][1]
            correct = 0.0
            for i in range(len(y)):
                if y[i] == res[i]:
                    correct += 1
            acc_test.append(correct / len(y))
            res = t.predict(part[r]["train"][0])
            y = part[r]["train"][1]
            correct = 0.0
            for i in range(len(y)):
                if y[i] == res[i]:
                    correct += 1
            acc_train.append(correct / len(y))
        print("Accuracy(train):" + str(acc_train[-1]))
        print("Accuracy(test):" + str(acc_test[-1]))
        print("-----------------------")
        accRate["train"].append(sum(acc_train) / 3)
        accRate["test"].append(sum(acc_test) / 3)
    plt.plot(depths, accRate["train"], label = "Training Accuracy")
    plt.plot(depths, accRate["test"], label = "Testing Accuracy" )
    plt.ylabel('Accuracy')
    plt.xlabel('Depth')
    plt.legend()
    pp = PdfPages('validation.pdf')
    plt.savefig(pp, format='pdf')
    pp.savefig()
    pp.close()
    

    

if __name__ == "__main__":
    validation_curve()
