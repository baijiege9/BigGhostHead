# -*- coding:utf-8 -*-
import web_text
import urllib.request
from models import Langem
import time #time.sleep()
import re
from bs4 import BeautifulSoup

url = 'http://news.sina.com.cn/china/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
headers = { 'User-Agent' : user_agent }  
request = urllib.request.Request(url=url,headers=headers, method = 'GET') 
response = urllib.request.urlopen(request)
page = response.read().decode('utf-8')
soup = BeautifulSoup(page, 'lxml')
time = time.localtime(time.time())
url_time = tranform(time.tm_year)+'-'+tranform(time.tm_mon)+'-'+tranform(time.tm_mday)
for a in soup.find_all('a'):
	if url_time in str(a):
		title = BeautifulSoup(urllib.request.urlopen(a.get('href')).read(), 'lxml').title.text
		content = urllib.request.urlopen(a.get('href')).read().decode('utf-8')
		content = web_text.extract(content)
		langem = Langem(title=title.strip(), content=content.strip())
		langem.save()

def tranform(int):
	if int<10:
		return '0'+str(int)
	else:
		return str(int)