#include<iostream>
#include<fstream>
#include<vector>
#include<set>
#include<sstream>
#include<cmath>
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

double s2f(string s)
{
	return atof(s.c_str());
}
vector<int> train;
vector<int> pre;
vector<double> weight;
vector<double> w;
bool t[SIZE];
vector<string> para[7000];
bool ans[7000];
bool test_ans[7000];
double ans_count[7000][2];
double B[100];
bool train_ans[6000];
int vote[100];
void genTest()
{
	ofstream fout2("predict");
	for(int i = 0; i < pre.size(); i++)
	{
		int id = pre[i];
		if((para[id].back())[0] == 's')
		{
			ans[i] = 1;
			fout2 << 1;
		}
		else
		{
			fout2 << 0;
			ans[i] = 0;
		}
		for(int j = 0; j < para[id].size() - 1; j++) 
		{
			fout2<<" "<<j+1<<":"<<para[id][j];
		}
		fout2<<endl;
	}
	fout2.close();
}

void getres(string name)
{
	cout<<name<<endl;
	ifstream fin(name.c_str());
	string line;
	double small = 0, big = 0;
	int count = 0;
	while(count < pre.size())
	{
		int i2;
		fin >> i2;
		if(ans[count] == i2) small ++;
		big++;
		count++;
	}
	cout<<"Accuracy : "<< small / big * 100 << "%"<<endl;
}

void check()
{
	double small = 0, big = 0;
	for(int i = 0; i < pre.size(); i++)
	{
		small += (test_ans[i] == ans[i]);
			big++;
	}
	cout<<"Accuracy : "<< small / big * 100 << "%"<<endl;
}


void normalize()
{
	double sum = 0;
	for(int i = 0; i < train.size(); i ++)
		sum += weight[i];
	for(int i = 0; i < train.size(); i ++)
		weight[i] /= (sum / train.size());
}

void genWeight()
{
	ofstream out("weight");
	for(int i = 0; i< train.size(); i++)
		out<<weight[i]<<endl;
	out.close();
}

void changeWeight(int t,string name)
{
	bool ok[6000];
	ifstream fin(name.c_str());
	string line;
	double small = 0, big = 0,Et = 0;
	int count = 0;
	//cout<<name<<endl;
	//normalize();
	while(count < train.size())
	{
		int i2;
		fin >> i2;
		if(train_ans[count] != i2)
		{
			ok[count] = 0;
			Et += weight[count];
		}
		else
		{
			ok[count] = 1;
			small ++;
		}
		count++;
	}
	B[t] = Et / ( train.size() - Et );
	cout<< Et <<endl;
	for(int i = 0; i < train.size(); i++)
		if(ok[i]) weight[i] *= B[t];
	normalize();
	if(small / train.size() < 0.6) vote[t] = 0;
	else vote[t] = 1;
	return;
}

int main()
{
	srand((unsigned)time(NULL));
	string line;
	ifstream fin("ContentNewLinkAllSample.csv");
	int count = 0;
	int trainsize = SIZE/5*4;
	getline(fin,line);
	for(int i = 0;i < trainsize; i++) t[i] = 1;
	for(int i = 0; i < 1000000; i++)
	{
		int idx1 = rand()%6214, idx2 = rand()%6214;
		swap(t[idx1],t[idx2]);
	}
	for(int i = 0; i < SIZE; i++) 
		if(t[i]) train.push_back(i);
		else pre.push_back(i);
	for(int i = 0; i < train.size(); i++)
		weight.push_back(1.0);
	while(getline(fin,line))
	{
		para[count] = split(line,",");
		count++;
	}
	int time = 20;
	cout<<"Input T"<<endl;
	cin>>time;
	string name[100];
	system("rm ./svm/*");
	genTest();
	ofstream fout("train");
	for(int i = 0; i < train.size(); i++)
	{
		int id = train[i];
		if((para[id].back())[0] == 's')
		{
			fout<<1;
			train_ans[i] = 1;
		}
		else
		{
			fout<<0;
			train_ans[i] = 0;
		}
		for(int j = 0; j < para[id].size() - 1; j++) fout<<" "<<j+1<<":"<<para[id][j];
		fout<<endl;
	}
	fout.close();
	genWeight();
	system("./libsvm_w/svm-scale train >>train_scale");
	system("./libsvm_w/svm-scale predict >>predict_scale");
	system("./libsvm_w/svm-train -h 0 train_scale");
	system("./libsvm_w/svm-predict predict_scale train_scale.model ./svm/svm");
	system("rm train");system("rm train_scale");system("rm train_scale.model");
	for(int i = 0; i < time; i++)
	{
		cout<<"Time: "<<i<<endl;
		string prec = "./libsvm_w/svm-predict predict_scale train_scale.model ";
		stringstream ss;
		ss << "./svm/svm_" << i;
		name[i] = ss.str();
		prec += name[i];
		ofstream fout("train");
		for(int i = 0; i < train.size(); i++)
		{
			int id = train[i];
			if((para[id].back())[0] == 's')
			{
				fout<<1;
				train_ans[i] = 1;
			}
			else
			{
				fout<<0;
				train_ans[i] = 0;
			}
			for(int j = 0; j < para[id].size() - 1; j++) fout<<" "<<j+1<<":"<<para[id][j];
			fout<<endl;
		}
		fout.close();
		system("./libsvm_w/svm-scale train >>train_scale");
		system("./libsvm_w/svm-train -W weight -h 0 train_scale");
		system("./libsvm_w/svm-predict train_scale train_scale.model res");
		system(prec.c_str());
		changeWeight(i,"res");
		genWeight();
		system("rm res");
		system("rm train");system("rm train_scale");system("rm train_scale.model");
	}
	cout<<"************************************"<<endl;
	cout<<"Orginal SVM"<<endl;
	getres("./svm/svm");
	for(int i = 0; i < time; i++)
	{
		count = 0;
		ifstream fin(name[i].c_str());
		while(count < pre.size())
		{
			int i2;
			fin >> i2 ;
			ans_count[count][i2] += log(1/B[i]) * vote[i];
			count++;
		}
	}
	for(int i = 0; i < pre.size(); i++)
	{
		//cout<<ans_count[i][1]<<" - "<<ans_count[i][0]<<endl;
		if(ans_count[i][1] <= ans_count[i][0]) test_ans[i] = 0;
		else test_ans[i] = 1;
	}
	cout<<"AdaBoost.M1+SVM:"<<endl;
	check();
	system("rm predict");system("rm predict_scale");
}
			
			
	
	
