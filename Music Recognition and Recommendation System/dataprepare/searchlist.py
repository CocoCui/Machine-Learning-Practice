#coding:utf-8
import random
import urllib2
import time
import re
import sys
import os

link = re.compile('href="/playlist\?id=(\d+?)"')
proxylist = ['183.218.63.174:8118','117.177.246.144:81','27.202.171.150:80','60.165.46.21:55336','139.214.113.74:55336','218.56.172.23:80','183.207.229.138:82','61.178.248.167:55336','111.127.107.61:80','121.43.225.134:9999']
urlbase = 'http://music.163.com'

def searchlist(num):
	url = urlbase + '/discover/playlist/?order=hot&cat=%E5%B0%8F%E8%AF%AD%E7%A7%8D&limit=35&offset='+str(num)
	request = urllib2.Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
	html = ''
	
	while True:
		try: 
			proxynum = random.randint(0, len(proxylist)-1)
			proxy = urllib2.ProxyHandler({'http':proxylist[proxynum]})
			opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)
			urllib2.install_opener(opener)
			html= opener.open(request).read()#.decode('utf-8')
			break
		except urllib2.URLError, e:  
			if hasattr(e, 'code'):
				print e.code
				if e.code == 404:
					return 0
				else:
					continue
			else:
				print e
				continue
	findings = link.findall(html)
	f = open('list','a')
	for i in range (0, len(findings)/2):
		f.write(findings[i*2])
		f.write('\n')
	return len(findings)


if __name__ == '__main__':
	for i in range(0,200):
		print i
		if searchlist(i*35) == 0:
			break