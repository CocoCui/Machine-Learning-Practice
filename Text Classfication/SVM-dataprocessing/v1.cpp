#include<iostream>
#include<fstream>
#include<cstdio>
#include<string.h>
#include<cstdlib>
#include<sstream>
#include<cmath>
#include<vector>
using namespace std;
struct word_info
{
	double A;
	double B;
	double C;
	double D;
	int word_idx;
	double v;
} wordbook[20000][4],temp[20000];

string path;
bool voc[60000001];
int wordhash[60000001];
int findword[60000001];
int type_check[600010];
int tot_word;
int tot_source;
vector<int> source[500];
int wordlist[10000];
double df[10000];
double idf[10000];
int start[4] = {-1,-1,-1,-1};
int length;

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
			if(voc[idx] == 0)
			{
				voc[idx] = 1;
				wordhash[idx] = tot_word;
				for(int i = 0;i<4;i++)
					wordbook[tot_word][i].word_idx =idx;
			   tot_word++;	
			}

		}
		word.clear();
	}
}

void work(int idx)
{
	int type = source[idx][0];
	bool flag[20000];
	for(int i = 0;i<20000;i++)
		flag[i] = 0;
	int num;
	for(int i = 1;i<source[idx].size();i++)
	{
		num = wordhash[source[idx][i]];
		flag[num] = 1;
	}
	for(int i = 0;i<tot_word;i++)
	{
		if(flag[i])
		{
			wordbook[i][type].A++;
			for(int j = 0;j<4;j++)
			{
				if(j == type) continue;
				wordbook[i][j].B++;
			}

		}
		else
		{
			wordbook[i][type].C++;
			for(int j = 0;j<4;j++)
			{
				if(j == type) continue;
				wordbook[i][j].D++;
			}
		}
	}
}

void cal_v()
{
	for(int i = 0;i<4;i++)
		for(int j = 0;j<tot_word;j++)
		{
			double A = wordbook[j][i].A;
			double B = wordbook[j][i].B;
			double C = wordbook[j][i].C;
			double D = wordbook[j][i].D;
			wordbook[j][i].v = (A*D-B*C)*(A*D-B*C)/((A+C)*(A+B)*(B+D)*(C+D));
		}
}
int cmp(const void* a,const void* b)
{
	if( ((word_info*)a)->v >= ((word_info*)b)->v ) return -1;
	else return 1;
}	

void choose(int type,int num)
{
	for(int i = 0;i<tot_word;i++)
	{
		temp[i].v = wordbook[i][type].v;
		temp[i].A = wordbook[i][type].A;
		temp[i].B = wordbook[i][type].B;
		temp[i].C = wordbook[i][type].C;
		temp[i].D = wordbook[i][type].D;
		temp[i].word_idx = wordbook[i][type].word_idx;
	}
	qsort(temp,tot_word,sizeof(word_info),cmp);
	for(int i = type*num;i<(type+1)*num;i++)
	{
		wordlist[i] = temp[i].word_idx;
		//random choose
		//wordlist[i] = temp[rand()%tot_word].word_idx;
		findword[wordlist[i]] = i;
		df[i] = temp[i].A + temp[i].B;
		idf[i] = log(tot_source/df[i]);
	}
}

void output(int type, int num)
{
	double vec[20000];
	double sum = 0;
	for(int i = 0; i<20000 ; i++) vec[i] = 0;
	for(int i = start[type];i < start[type] + num; i++)
	{
		for(int j = 0; j<20000 ; j++) vec[j] = 0;
		for(int j = 0; j < source[i].size() ; j++)
		{
			if(findword[source[i][j]])
			{
				vec[findword[source[i][j]]]++;
			}
		}
		cout<<type<<" ";
        for(int i = 0;i<length;i++)
		{
			// w = tf * idf;
			vec[i] = vec[i] * idf[i];
		}
		for(int i = 0;i<length;i++)
			cout<<i<<":"<<vec[i]<<" ";
		cout << endl;
	}
	return;		
}

int main()
{
	string tot_path,idx;
	int count = 0;
    cout<<"特征单词数："<<endl;
    cin>>length;
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
	for(int i = 0;i<tot_source;i++)work(i);
	cal_v();
	for(int i = 0;i<4;i++)
	{
		choose(i,length/4);
	}
	//cout<<tot_word<<endl;
	//choose(0,tot_word);
	for(int j = 10;j<=100;j+= 10)
	{
		string num,file_name;
		stringstream change;
		change << j;
		change >> num;
		file_name = num;
		freopen(file_name.c_str(),"w",stdout);
		for(int i = 0;i < 4;i++)output(i,j);
	}
	freopen("all","w",stdout);
	for(int i = 0;i < 4;i++)output(i,100);
	return 0;
}


