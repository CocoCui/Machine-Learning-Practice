#coding:utf-8
import math

if __name__ == '__main__':

	d = {}
	simdict = {}
	songdict = {}
	f = open('songlist')
	s = f.readline().strip()
	while s:
		parts = s.split('\t')
		songdict[parts[0]] = parts[1]
		s = f.readline().strip()
	f.close()
	f = open('music')
	s = f.readline().strip()
	while s:
		parts = s.split('|')
		infolist = parts[1].split(' ')
		d[parts[0]] = set()
		for info in infolist:
			if info == '':
				continue
			else:
				d[parts[0]].add(info)
		s = f.readline().strip()
	f.close()


	f = open('recommendall','w')
	for songname in d.keys():
		f.write(songdict[songname] + ' ')
		print songname
		vector = d[songname]
		for key in d.keys():
			if key == songname:
				continue
			else:
				simdict[key] = len(d[key] & vector)/math.sqrt(len(vector) * len(d[key]))
		res = sorted(simdict.items(), key=lambda x:x[1], reverse = True)
		for i in range(0,20):
			f.write(songdict[res[i][0]] + ' ')
		f.write('\n')
	f.close()
