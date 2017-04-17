#include<iostream>
#include<fstream>
#include<cstdio>
#include<string.h>
#include<cstdlib>
#include<sstream>
#include<vector>

using namespace std;

string path;
bool voc[60000001];
double wordlist[60000001][4];
int tot_word[4];
int tot;
int tot_test;
int right_test;
int tot_source;
int start[4] = {-1,-1,-1,-1};
vector<int> source[500];

int judge(char in)
{
	if((in>='a'&&in<='z')||(in>='A'&&in<='Z')) return 1;
	else return 0;
}

unsigned int Hash(string input)
{
    unsigned int seed = 131; // 31 131 1313 13131 131313 etc..
    unsigned int hash = 0;
	int idx = 0;
	int len = strlen(input.c_str());
    while (idx<len)
    {
        hash = hash * seed + (input[idx++]);
    }
    return (hash & 0x7FFFFFFF)%60000001;
}

void input(int type,int source_idx)
{
	char temp;
	string word;
	int idx;
	int wordcount = 1;
	source[source_idx].push_back(type);
	while(temp > -1) 
	{
		temp = getchar();
		while(judge(temp) && temp > -1)
		{
			if(temp<=90) temp += 32;
			word += temp;
			temp = getchar();
		}
		if(strlen(word.c_str())>4) 
		{
			idx = Hash(word);
			source[source_idx].push_back(idx);
		}
		word.clear();
	}
}

void setword(int type,int idx)
{
	int word_idx;
	for(int i = 1;i<source[idx].size();i++)
	{
		word_idx = source[idx][i];
		voc[word_idx] = 1; 
		wordlist[word_idx][type]++;
		tot_word[type]++;
		tot++;
	}
}

int check(int idx)
{
	char temp;
	string word;
	double max_p = -1;
	int type,word_idx;
	double p[4] = {1,1,1,1};
	for(int i = 0;i<source[idx].size();i++)
	{
		word_idx = source[idx][i];
		if(voc[word_idx])
		{
			for(int i = 0;i<4;i++)
			{
				p[i]=p[i]*wordlist[word_idx][i];
				if(p[i]>100000000) 
				for(int j = 0;j < 4;j++)
					p[j]/=10000;
			}
		}
	}
	for(int i = 0;i<4;i++)
	{
		if(p[i]>max_p) 
		{
			max_p = p[i];
			type =i;
		}
	}
	return type;
}

int main()
{
	string tot_path,idx; 
	int count = 0;
	int train_num = 100;
	for(int i = 0;i<4;i++)
	{
		if(i == 0) path = "c1/";
		if(i == 1) path = "c2/";
		if(i == 2) path = "c3/";
		if(i == 3) path = "c4/";
		count = 0;
		while(count<600000)
		{
			stringstream change;
			change << count;
			change >> idx;
			tot_path = path + idx;
			while(!freopen(tot_path.c_str(),"r",stdin) && count <600000)
			{
				count++;
				stringstream change;
				change << count;
				change >> idx;
				tot_path = path + idx;
			}
			if(freopen(tot_path.c_str(),"r",stdin))
			{
				input(i,tot_source);
				if(start[i]<0) start[i] = tot_source;
				tot_source++;
			}
			count++;
		}
	}
	freopen("Result.txt","w",stdout);
	for(train_num = 10; train_num <= 100; train_num += 10)
	{
		cout<<train_num<<"% of data for train:"<<endl;
		tot = 0,tot_test = 0,right_test = 0;
		int t0 = 0;
		for(int i = 0;i<4;i++) tot_word[i]=0;
		for(int i = 0;i<4;i++)
			for(int j = 0;j<60000001;j++)
			{
				wordlist[j][i] = 0;
				voc[j] = 0;
			}
		for(int i = 0;i<4;i++)
			for(int j = start[i];j<train_num+start[i];j++) setword(i,j);
		for(int i = 0;i<4;i++)
			for(int j = 0;j<60000001;j++)
				if(voc[j]) wordlist[j][i] = (wordlist[j][i]+1)/(tot_word[i]+tot/5)*10000;
		for(int i = 0;i<4;i++)
		for(int j = start[i];j<train_num+start[i];j++) 
		{
			tot_test++;
			if(check(j) == source[j][0]) right_test++;
		}
		for(int i = 0 ; i< 400 ;i++)
			if(check(i) == source[i][0]) t0++;
		cout<<"回归率:"<<double(right_test)/double(tot_test)*100.0<<endl;
		cout<<"准确率（全部数据）:"<<double(t0)/400.0*100.0<<endl;
		if(400-train_num*4 == 0) cout<<"准确率（交叉测试）: NULL"<<endl;
		else cout<<"准确率（交叉测试）:"<<double(t0 -right_test)/double(400-train_num*4)*100.0<<endl;
	}
	return 0;
}

