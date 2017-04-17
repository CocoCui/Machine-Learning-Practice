#include<iostream>
#include<fstream>
#include<vector>
#include<set>
#include<sstream>
#define SIZE 6214
using namespace std;

vector<string> split(string& s,string delim)
{
	vector< string > ret;
	size_t last = 0;
	size_t index=s.find_first_of(delim,last);
	while (index!=std::string::npos)
	{
		ret.push_back(s.substr(last,index-last));
		last=index+1;
		index=s.find_first_of(delim,last);
	}
	if (index-last>0)
	{
		ret.push_back(s.substr(last,index-last));
	}
	return ret;
}

float s2f(string s)
{
	return atof(s.c_str());
}
vector<int> train;
vector<int> pre;
bool t[SIZE];
vector<string> para[7000];
bool ans[7000];
bool test_ans[7000];
int ans_count[7000][2];

void check()
{
	float small = 0, big = 0;
	for(int i = 0; i < pre.size(); i++)
	{
		small += (test_ans[i] == ans[i]);
		big++;
	}
	cout<<"Accuracy : "<< small / big * 100 << "%"<<endl;
}

int main()
{
	srand((unsigned)time(NULL));
	string line;
	ifstream fin("ContentNewLinkAllSample.csv");
	ofstream fout1("predict.csv");
	int count = 0;
	int trainsize = SIZE/5*4;
	getline(fin,line);
	int num0 = 0,num1 = 0;
	for(int i = 0;i < trainsize; i++) t[i] = 1;
	for(int i = 0; i < 1000000; i++)
	{
		int idx1 = rand()%6214, idx2 = rand()%6214;
		swap(t[idx1],t[idx2]);
	}
	for(int i = 0; i < SIZE; i++) 
		if(t[i]) train.push_back(i);
		else pre.push_back(i);
	while(getline(fin,line))
	{
		para[count] = split(line,",");
		count++;
	}
	int time = 10;
	cout<<"Input T"<<endl;
	cin>>time;
	for(int i = 0; i < pre.size(); i++)
	{
		int id = pre[i];
		if((para[id].back())[0] == 's')
		{
			ans[i] = 1;
			fout1 << 1;
		}
		else
		{
			fout1 << 0;
			ans[i] = 0;
		}
		for(int j = 0; j < para[id].size() - 1; j++) fout1<<" "<<j+1<<":"<<para[id][j];
		fout1<<endl;
	}
	fout1.close();
	ofstream fout("train.csv");
	for(int i = 0; i < train.size(); i++)
	{
		int id = train[i];
		if((para[id].back())[0] == 's') fout<<1;
		else fout<<0;
		for(int j = 0; j < para[id].size() - 1; j++) fout<<" "<<j+1<<":"<<para[id][j];
		fout<<endl;
	}
	fout.close();
	system("./libsvm/svm-scale train.csv >>train_scale.csv");
	system("./libsvm/svm-scale predict.csv >>predict_scale.csv");
	system("./libsvm/svm-train -h 0 train_scale.csv");
	system("./libsvm/svm-predict predict_scale.csv train_scale.csv.model ./svm/svm");
	string name[100];
	for(int i = 0; i < time; i++)
	{
		cout<<"Time: "<<i<<endl;
		string prec = "./libsvm/svm-predict predict_scale.csv train_scale.csv.model ";
		stringstream ss;
		ss << "./svm/svm" << i;
		name[i] = ss.str();
		prec += name[i];
		set<int> trainset;
		int time = 0;
		while(time < 3000)
		{
			int idx = rand() % train.size();
			trainset.insert(train[idx]);
			time++;
		}
		ofstream fout("train.csv");
		for(set<int>::iterator it = trainset.begin(); it != trainset.end(); it++)
		{
			int id = *it;
			if((para[id].back())[0] == 's') fout<<1;
			else fout<<0;
			for(int j = 0; j < para[id].size() - 1; j++) fout<<" "<<j+1<<":"<<para[id][j];
			fout<<endl;
		}
		fout.close();
		system("rm train_scale.csv");
		system("./libsvm/svm-scale train.csv >>train_scale.csv");
		system("./libsvm/svm-train -h 0 train_scale.csv");
		system(prec.c_str());
	}
	system("rm train.csv");system("rm train_scale.csv");system("rm train_scale.csv.model");
	system("rm predict.csv");system("rm predict_scale.csv");
	ifstream fin1("./svm/svm");
	count = 0;
	while(count < pre.size())
	{
		fin1>>test_ans[count];
		count++;
	}
	cout<<"**********************************************"<<endl;
	cout<<"Orginal SVM:"<<endl;
	check();
	for(int i = 0; i < time; i++)
	{
		count = 0;
		ifstream fin(name[i].c_str());
		while(count < pre.size())
		{
			int id;
			fin>>id;
			ans_count[count][id]++;
			count++;
		}
	}
	for(int i = 0; i < pre.size(); i++)
	{
		if(ans_count[i][1] < ans_count[i][0]) test_ans[i] = 0;
		else test_ans[i] = 1;
	}
	cout<<"SVM+Bagging:"<<endl;
	check();
}
			
			
	
	
