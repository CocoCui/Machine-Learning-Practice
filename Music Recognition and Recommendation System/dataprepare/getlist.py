#coding:utf-8
import random
import socket
import urllib
import urllib2
import time
import re
import sys
import os

#proxylist = ['220.134.222.34:8888','211.142.197.130:80','111.127.107.61:80','117.163.37.246:8123','120.206.190.85:8123','139.214.113.74:55336','218.244.133.29:43629','183.218.63.174:8118','117.177.246.144:81','60.165.46.21:55336','139.214.113.74:55336','218.56.172.23:80','183.207.229.138:82','61.178.248.167:55336','111.127.107.61:80','121.43.225.134:9999']
proxylist = []
proxynum = 0
urlbase = 'http://music.163.com/playlist?id='
song = re.compile('<a href="/song\?id=(\d+)">(.+?)</a>')
tagpattern = re.compile('<a class="u-tag" href=".*?"><i>(.*?)</i></a>')
composer = re.compile('<a class="s-fc7" href="/artist\?id=\d+">(.*?)</a>')
composer1 = re.compile('<p class="des s-fc4">歌手：<span title=".*?"><span class="s-fc7".*?>(.*?)</span></span></p>')
code = re.compile('"mp3Url":"(.*?)","rtUrls":null,"name":"(.*?)","id":(\d+)')
def findcomposer(id):
	global proxynum
	url = 'http://music.163.com/song?id=' + id
	print url
	request = urllib2.Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	html = ''
	while True:
		try: 
			proxy = urllib2.ProxyHandler({'http':proxylist[proxynum]})
			opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
			urllib2.install_opener(opener)
			html= opener.open(request,timeout = 5).read()#.decode('utf-8')
			break
		except Exception, e:
			proxynum = random.randint(0, len(proxylist)-1)
			print e
			print proxylist[proxynum]
			continue

	''''''
	findings = composer.findall(html)
	if len(findings) == 0:
		return composer1.findall(html)
	return findings



def getinfo(s):
	global proxynum
	url = urlbase + s
	request = urllib2.Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	html = ''
	print s
	while True:
		try: 
			proxy = urllib2.ProxyHandler({'http':proxylist[proxynum]})
			opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
			urllib2.install_opener(opener)
			html= opener.open(request,timeout = 5).read()#.decode('utf-8')
			break
		except Exception, e:
			print proxylist[proxynum]
			proxynum = random.randint(0, len(proxylist)-1)
			print e
			continue
	f = open('./list/'+s,'w')
	f.write('TAGS:')
	tags = tagpattern.findall(html)
	for tag in tags:
		f.write(tag+';')
	f.write('\n')

	res = code.findall(html)
	#l = list(set(code.findall(html)))
	

	for info in res:
		writername = ''
		f.write(info[1] + '\t')
		writerlist = findcomposer(info[2])
		f.write('\t')

		for writer in writerlist:
			f.write(writer+'/')
			writername = writername + '_' + writer
		f.write('\n')
		'''
		while True:
			try: 
				proxy = urllib2.ProxyHandler({'http':proxylist[proxynum]})
				opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
				urllib2.install_opener(opener)
				socket.setdefaulttimeout(5)
				urllib.urlretrieve(info[0],'./music/' + info[1] + writername + '.mp3')
				break
			except Exception, e:
				proxynum = random.randint(0, len(proxylist)-1)
				print e
				continue
		'''
		while True:
			try: 
				proxy = urllib2.ProxyHandler({'http':proxylist[proxynum]})
				opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
				urllib2.install_opener(opener)
				music= opener.open(info[0],timeout = 5).read()#.decode('utf-8')
				break
			except Exception, e:
				proxynum = random.randint(0, len(proxylist)-1)
				print e
				print proxylist[proxynum]
				continue
		m = open('./music/' + info[1] + writername + '.mp3','w')
		m.write(music)
		m.close()
	f.close()



if __name__ == '__main__':
	#filenames = ['Chinese','Europe_America','Japanese','Korean','Others']
	f = open('ip.txt')
	s = f.readline().strip()
	while s:
		proxylist.append(s)
		s = f.readline().strip()
	f.close()

	filenames = ['fix']
	listset = set()
	for filename in filenames:
		f = open(filename)
		s = f.readline().strip()
		while s:
			listset.add(s)
			s = f.readline().strip()
	l = list(listset)
	st = int(raw_input())
	ed = int(raw_input())
	proxynum = random.randint(0, len(proxylist)-1)
	for i in range(st,ed):
		print i
		getinfo(l[i])