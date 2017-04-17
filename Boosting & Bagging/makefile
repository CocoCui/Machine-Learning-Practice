all: bagging_c50 bagging_svm bagging_svm_n boosting_svm boosting_c50
	g++ bagging_c50.cpp -o bagging_c50
	g++ bagging_svm.cpp -o bagging_svm
	g++ bagging_svm_n.cpp -o bagging_svm_n
	g++ boosting_c50.cpp -o boosting_c50
	g++ boosting_svm.cpp -o boosting_svm
	cd ./libsvm && make
	cd ./libsvm_w && make
	cd ./C50 && make
	cd ./C50 && g++ ./see5-public/sample.c -o sample
clean:
	rm bagging_c50 bagging_svm bagging_svm_n boosting_svm boosting_c50
