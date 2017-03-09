#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import mysql.connector

__author__ = 'Bai Jie'

def list_str(Ilist):
	Ilist = str(Ilist)
	Ilist = Ilist.replace("[", "")
	Ilist = Ilist.replace("]", "")
	Ilist = Ilist.replace("'","")
	return Ilist

def save_mysql(url, title, source, time, centent, classification):
		conn = mysql.connector.connect(user = 'root', password = 'yqdhgqd99', database = 'huizhouspider')
		cursor = conn.cursor()
		url = list_str(url)
		title = list_str(title)
		source = list_str(source)
		time = list_str(time)
		centent = list_str(centent)
		cursor.execute("insert into news (Sourcesites, title, source, publishtime, content, classification) values (%s, %s, %s, %s, %s, %s)", [url, title, source, time, centent, classification])
		cursor.rowcount
		conn.commit()
		print( '成功存入一条数据url:' + url )
		cursor.close()
		conn.close()

def saveFile(data, save_name):
	save_path = str(save_name) +'.html'
	f_obj = open(save_path, 'w',encoding = 'utf-8')
	f_obj.write(data)
	f_obj.close()

def SaveVisited(Iset):
	txt = str(Iset)
	txt = txt.replace("{","")
	txt = txt.replace("}","")+"\n"
	File = open("visited.txt","w")
	File.write(txt)
	File.close()
	print("保存visited成功")

def RoadVisited():
	File = open("visited.txt","r") 
	i = File.readline() #读取文件内容
	i = i.replace("\n","")
	Line = i.split(",")#将,作为切分点
	Iset = set( Line )
	print( "当前visited为" + str(Iset) )
	return Iset

def getTitle(data):#一定要字符，不能是二进制数据，可用decode()转换
	if type(data) != str:
		print("白睫哥提醒您： cannot use a string pattern on a bytes-like object")
	linkre = re.compile( r"<td class='artTitle'>(.+)" )
	return linkre.findall(data)#返回一个列表
	if linkre.findall(data) == []:
		print("此页面没有任何标题")

def getSource(data):
	if type(data) != str:
		print("白睫哥提醒您： cannot use a string pattern on a bytes-like object")
	linkre = re.compile( r"<div class='artSource'>(.+)</div>" )
	return linkre.findall(data)
	if linkre.findall(data) == []:
		print("此数据没有任何文字来源")

def getTime(data):
	if type(data) != str:
		print("白睫哥提醒您： cannot use a string pattern on a bytes-like object")
	linkre = re.compile( r"(发布时间：.+)</td>" )
	return linkre.findall(data)
	if linkre.findall(data) == []:
		print("此数据没有任何时间")

def getCentent(data):
	if type(data) != str:
		print("白睫哥提醒您： cannot use a string pattern on a bytes-like object")
	linkre = re.compile( "<td class='artContent'>(.*?) </td>",re.DOTALL )
	return linkre.findall(data)
	if linkre.findall(data) == []:
		print("此数据没有任何文章内容")

f = open('word_chinese.txt', 'r', encoding = 'utf-8')#加载抓取类必须的字典
find_dict = {}
for line in f:
	line = line.replace('\n', '')
	values,key = line.split('：')
	find_dict[key] = values

def getClassification(url):
	for key in find_dict:
		if key in url.split('/'):
			return find_dict[key]

def getYuanXiaoMingCheng(data):
	linkre = re.compile( "\<a title=\"点击查看院校信息\" target=\"\_blank\" href=\".*?\"\>(.+?)\</a>[\s\S]*?<td>(.+?)</td>")
	return linkre.findall(data)