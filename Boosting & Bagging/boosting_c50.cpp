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

void genTest()
{
	ofstream fout2("data.cases");
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
		fout2<<",1";
		for(int j = 0; j < para[id].size() - 1; j++) 
		{
			fout2<<","<<para[id][j];
		}
		fout2<<endl;
	}
	fout2.close();
}

void getres(string name)
{
	ifstream fin(name.c_str());
	string line;
	double small = 0, big = 0;
	getline(fin,line);
	getline(fin,line);
	getline(fin,line);
	int count = 0;
	while(count < pre.size())
	{
		string p;
		int num = 0;
		int i1,i2;
		fin >> num >> i1 >> i2 >> p;
		if(i1 == i2) small ++;
		big++;
		count++;
	}
	cout<<"Accuracy : "<< small / big * 100 << "%("<<small<<"/"<<big<<")"<<endl;
}

void genWeight()
{
	ofstream out("weight");
	for(int i = 0; i< train.size(); i++)
		out<<weight[i]<<endl;
	out.close();
}

void check()
{
	double small = 0, big = 0;
	for(int i = 0; i < pre.size(); i++)
	{
		small += (test_ans[i] == ans[i]);
		big++;
	}
	cout<<"Accuracy : "<< small / big * 100 << "%("<<small<<"/"<<big<<")"<<endl;
}


void normalize()
{
	double sum = 0;
	for(int i = 0; i < train.size(); i ++)
		sum += weight[i];
	for(int i = 0; i < train.size(); i ++)
		weight[i] /= (sum / train.size());
}
	
void changeWeight(int t,string name)
{
	bool ok[6000];
	ifstream fin(name.c_str());
	string line;
	double small = 0, big = 0,Et = 0;
	getline(fin,line);
	getline(fin,line);
	getline(fin,line);
	int count = 0;
	while(count < train.size())
	{
		string p;
		int num;
		int i1,i2;
		fin >> num >> i1 >> i2 >> p;
		if(i1 != i2)
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
	cout<< Et <<" Bt "<< B[t]<< endl;
	for(int i = 0; i < train.size(); i++)
		if(ok[i]) weight[i] *= B[t];
	normalize();
	genWeight();
	cout<<"Accuracy : "<< small / train.size() * 100 << "%("<<small<<"/"<<train.size()<<")"<<endl;
	return;
}

int main()
{
	srand((unsigned)time(NULL));
	string line;
	ifstream fin("ContentNewLinkAllSample.csv");
	ofstream nf("data.names");
	int count = 0;
	int trainsize = SIZE/5*4;
	getline(fin,line);
	vector<string> p = split(line,",");
	nf<<"type."<<endl;
	nf<<"type"<<": "<<"1, 0."<<endl;
	nf<<"case weight: "<<"continuous."<<endl;
	for(int i = 0; i < p.size() - 1; i++)
		nf<<p[i]<<": "<<"continuous."<<endl;
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
	int time = 50;
	cout<<"Input T"<<endl;
	cin>>time;
	string name[100];
	system("rm ./c50res/*");
	genTest();
	ofstream fout("data.data");
	for(int i = 0; i < train.size(); i++)
	{
		int id = train[i];
		if((para[id].back())[0] == 's') fout<<1;
		else fout<<0;
		fout<<",1";
		for(int j = 0; j < para[id].size() - 1; j++) fout<<","<<para[id][j];
		fout<<endl;
	}
	fout.close();
	system("./C50/c5.0 -f data >> data.out");
	system("./C50/sample -f data >> ./c50res/c50");
	for(int i = 0; i < time; i++)
	{
		cout<<"Time: "<<i<<endl;
		string prec_pre = "./C50/sample -f data >> ";
		stringstream ss;
		ss << "./c50res/c50_" << i;
		name[i] = ss.str();
		prec_pre += name[i];
		string prec_train = prec_pre + "train";
		ofstream fout("data.data");
		ofstream fout1("data.cases");
		for(int i = 0; i < train.size(); i++)
		{
			int id = train[i];
			if((para[id].back())[0] == 's')
			{
				fout<<1;
				fout1<<1;
			}
			else
			{
				fout<<0;
				fout1<<0;
			}
			fout<<","<<weight[i]; fout1<<","<<weight[i];
			for(int j = 0; j < para[id].size() - 1; j++) 
			{
				fout<<","<<para[id][j];
				fout1<<","<<para[id][j];
			}
			fout<<endl;
			fout1<<endl;
		}
		fout.close();
		fout1.close();
		system("./C50/c5.0 -f data >> data.out");
		system(prec_train.c_str());
		changeWeight(i,name[i]+"train");
		genTest();
		system(prec_pre.c_str());
		getres(name[i]);

	}
	system("rm data.*");
	cout<<"*********************************************************"<<endl;
	cout<<"Orginal C50:"<<endl;
	getres("./c50res/c50");
	for(int i = 0; i < time; i++)
	{
		count = 0;
		ifstream fin(name[i].c_str());
		getline(fin,line);
		getline(fin,line);
		getline(fin,line);
		while(count < pre.size())
		{
			string p;
			int num = 0;
			int i1,i2;
			fin >> num >> i1 >> i2 >> p;
			ans_count[count][i2] += log(1/B[i]);
			count++;
		}
	}
	for(int i = 0; i < pre.size(); i++)
	{
		//cout<<ans_count[i][1]<<" - "<<ans_count[i][0]<<endl;
		if(ans_count[i][1] <= ans_count[i][0]) test_ans[i] = 0;
		else test_ans[i] = 1;
	}
	cout<<"AdaBoost.M1+C50:"<<endl;
	check();
}
			
			
	
	
