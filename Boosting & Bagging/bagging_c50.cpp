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


void getres(string name)
{
	ifstream fin(name.c_str());
	string line;
	float small = 0, big = 0;
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
	cout<<"Accuracy : "<< small / big * 100 << "%"<<endl;
}

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
	ofstream fout1("data.test");
	ofstream fout2("data.cases");
	ofstream nf("data.names");
	int count = 0;
	int trainsize = SIZE/5*4;
	getline(fin,line);
	vector<string> p = split(line,",");
	nf<<"type."<<endl;
	nf<<"type"<<": "<<"1, 0."<<endl;
	for(int i = 0; i < p.size() - 1; i++)
	{
		nf<<p[i]<<": "<<"continuous."<<endl;
	}
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
	int time;
	cout<<"Input T"<<endl;
	cin>> time;
	system("rm ./c50res/*");
	for(int i = 0; i < pre.size(); i++)
	{
		int id = pre[i];
		if((para[id].back())[0] == 's')
		{
			ans[i] = 1;
			fout1 << 1;
			fout2 << 1;
		}
		else
		{
			fout1 << 0;
			fout2 << 0;
			ans[i] = 0;
		}
		for(int j = 0; j < para[id].size() - 1; j++) 
		{
			fout1<<","<<para[id][j];
			fout2<<","<<para[id][j];
		}
		fout1<<endl;
		fout2<<endl;
	}
	fout1.close();
	ofstream fout("data.data");
	for(int i = 0; i < train.size(); i++)
	{
		int id = train[i];
		if((para[id].back())[0] == 's') fout<<1;
		else fout<<0;
		for(int j = 0; j < para[id].size() - 1; j++) fout<<","<<para[id][j];
		fout<<endl;
	}
	fout.close();
	system("./C50/c5.0 -f data");
	system("./C50/sample -f data >> ./c50res/c50");
	string name[100];
	for(int i = 0; i < time; i++)
	{
		cout<<"Time: "<<i<<endl;
		string prec = "./C50/sample -f data >> ";
		stringstream ss;
		ss << "./c50res/c50_" << i;
		name[i] = ss.str();
		prec += name[i];
		set<int> trainset;
		while(trainset.size() < 2000)
		{
			int idx = rand() % train.size();
			trainset.insert(train[idx]);
		}
		ofstream fout("data.data");
		for(set<int>::iterator it = trainset.begin(); it != trainset.end(); it++)
		{
			int id = *it;
			if((para[id].back())[0] == 's') fout<<1;
			else fout<<0;
			for(int j = 0; j < para[id].size() - 1; j++) fout<<","<<para[id][j];
			fout<<endl;
		}
		fout.close();
		system("./C50/c5.0 -f data");
		system(prec.c_str());
	}
	system("rm data.*");
	cout<<"************************************************"<<endl;
	cout<<"Orignal C50:"<<endl;
	getres("./c50res/c50");
	for(int i = 0; i < time; i++)
	{
		count = 0;
		ifstream fin(name[i].c_str());
		getline(fin,line);
		getline(fin,line);
		while(count < pre.size())
		{
			string p;
			int num = 0;
			int i1,i2;
			fin >> num >> i1 >> i2 >> p;
			ans_count[count][i2]++;
			count++;
		}
	}
	for(int i = 0; i < pre.size(); i++)
	{
		if(ans_count[i][1] < ans_count[i][0]) test_ans[i] = 0;
		else test_ans[i] = 1;
	}
	cout<<"bagging+C50:"<<endl;
	check();
}
			
			
	
	
