##Practice of Ensemble Learning Algorithm

* libsvm：SVM
* libsvm_w：SVM with weighted samples
* svm：result of vm
* c50res：result of C5.0
* boosting_svm.cpp: SVM+AdaBoost.M1
* boosting_c50.cpp:C5.0+AdaBoost.M1
* bagging_svm.cpp:SVM+Bagging
* bagging_svm_n.cpp:SVM+Bagging(without feature normalization)
* bagging_c50.cpp:C5.0+Bagging(without feature normalization)
* ContentNewLinkAllSample.csv：data

-------------------
Result:

SVM: 88.36%   
C5.0:86.86%

Bagging+SVM: 89.01%   
Bagging+C5.0: 90.58%

Adaboost.M1 + SVM: 88.56%   
Adaboost.M1 + C5.0: 90.93%


