#coding:utf-8
import random
import urllib2
import time
import re
import sys
import os

if __name__ == '__main__':
	songdict = {}
	listdict = {}
	singerdict = {}
	infodict = {}
	tagdict = {}
	tagid = 9500
	songid = 0
	listid = 0
	singerid = 10000
	rootdir = './data/'
	num = 0
	for parent,dirnames,filenames in os.walk(rootdir):
		for filename in filenames:
			if filename == '.DS_Store':
				continue
			listdict[filename] = listid
			listid += 1
			fullname = os.path.join(parent,filename)
			f = open(fullname)
			s = f.readline().strip()
			tags = s.split(':')[1].split(';')
			for tag in tags:
				if tag == '':
					continue
				if tagdict.has_key(tag) == False:
					tagdict[tag] = tagid
					tagid += 1
			s = f.readline().strip()
			while s:
				res = s.split('\t\t')
				if infodict.has_key(res[0]) == False:
					infodict[res[0]] = set()
				infodict[res[0]].add(listdict[filename])
				if songdict.has_key(res[0]) == False:
					songdict[res[0]] = songid
					songid += 1
				singers = res[1].split('/')
				for singer in singers:
					if singer != '':
						if singerdict.has_key(singer) == False:
							singerdict[singer] = singerid
							singerid += 1
						infodict[res[0]].add(singerdict[singer])
				s = f.readline().strip()
			f.close()
	'''
	f = open('taglist','w')
	for key in tagdict:
		f.write(key + '\t' + str(tagdict[key]) + '\n')
	f.close()
	'''
	f = open('songlist','w')
	for key in songdict:
		f.write(key + '\t' + str(songdict[key]) + '\n')
	f.close()
	f = open('singerlist','w')
	for key in singerdict:
		f.write(key + '\t' + str(singerdict[key]) + '\n')
	f.close()
	f = open('list','w')
	for key in listdict:
		f.write(key + '\t' + str(listdict[key]) + '\n')
	f.close()
	f = open('infolist','w')
	w = open('music','w')
	for key in infodict:
		f.write(str(songdict[key]) + ' ')
		infolist = list(infodict[key])
		count = 0

		infolist.sort()
		for value in infolist:
			if value < 9500:
				count += 1
		if count > 8:
			num += 1
			w.write(key + '|')
			for value in infolist:
				if value < 9500:
					w.write(str(value) + ' ')
			w.write('\n')

		for value in infolist:
			f.write(str(value) + ' ')
		f.write('\n')
	f.close()
	w.close()
	print num