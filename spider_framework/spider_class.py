#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Python 标准库模块
# urllib.parse模块之前是用来写利用百度搜索引擎进行爬虫用到的，urllib.parse.urlencode(data)能将一个字典data转化为字符串。
# 例如data={'word':'Jecvay Notes'}转换为 'word=Jecvay+Notes'的字符串
# 这里是用来操作url的urllib模块里的抓取 请求的request模块
# deque是一个类似list的队列数据，操作类似，但是队列任务效率更高
#
import urllib.request
import urllib.parse
import re
import time
import random
from collections import deque
from urllib import request #这也是导入模块但是有个不同之处，一个代码中调用模块使用用request,一个是用urllib.request

# Python 第三方模块
import mysql.connector

# 应用程序自定义模块
# import tool

# 数据库类

# 网址类

# 变量类


class Identifiers(object):
    # 判定声明方法，返回值为真假
    def __init__(self):
        pass

    @staticmethod
    def isset(v):
        pass
# 爬虫类


class Spider(object):
    __author = 'Bai Jie Ge'

    # 表列名列表；数据库登陆列表；
    def __init__(self, spider_name, column_list, conn_list, *stop_url):
        self.spider_name = spider_name
        self.column_list = column_list
        self.conn_list = conn_list
        self.stop_url = stop_url
        self.queue_number = 0
        self.rule_instance_list = []
        self.linkre1 = re.compile('href=\"(.+?)\"')
        self.linkre2 = re.compile('href=\'(.+?)\'')

    # conn = mysql.connector.connect(user = 'root',password = 'password',database = 'test',table = '')
    # 各列名对应的一条记录的值。写入一条记录的方法.
    # column_dict参数格式是字典，采用列名 = 列名值的形式传入
    def write_mysql(self, column_dict):
        init_mysql = self.init_mysql()
        # 创建连接
        conn = mysql.connector.connect(user=self.conn_list[0], password=self.conn_list[1], database=self.conn_list[2])
        # 获取数据库连接对象cursor
        cursor = conn.cursor()
        # 初始化列名的值的列表
        column_value_list = []
        for column_key in self.column_list:
            column_value = column_dict[column_key]
            column_value_list.append(column_value)
        cursor.execute(init_mysql(), column_value_list)
        cursor.rowcount
        conn.commit()
        print('成功存入一条数据 %s', column_value_list)
        cursor.close()
        conn.close()

    # 初始化mysql的语句的静态方法，返回一个字符串。传入一个数据库table字符串参数，一个
    def init_mysql(self):
        table = self.conn_list[3]
        string1 = "insert into %s " % table
        column_string = ''
        counter = 0
        for column_name in self.column_list:
            # 防止int类型column（列名）无法进行string操作
            column_name = str(column_name)
            if counter == 0:
                column_string = column_name
                counter = 1
            else:
                column_string = column_string + ',' + column_name
        string2 = "(%s) values(%s)" % (column_string, len(self.column_list)*'%s,')
        # bug = string2[-2]
        new_string2 = ''
        # 为了筛选出字符串中那个该死的",",重新构造字符串.看不懂的话就consle看看string2[-2]
        for number in range(len(string2)):
            if number != len(string2)-2:
                # 我也不想用这么j8的写法，但是ide一直报错'assignment can be replaced with augmented assignment'
                temp = new_string2
                new_string2 = temp+string2[number]
        return string1 + new_string2

    def crawling(self, start_url):
        number = 0  # 计数
        queue = self.create_queue(start_url)
        visited = set()
        bug_url = set()  # 出错地址元表
        urlop = 'nill'
        while queue:
            column_dict = {}  # 清空并初始化一个dictionary
            url = queue.popleft()  # 从队列提取链接
            visited |= {url}
            print('已经抓取：' + str(number) + '     正在抓取 <--' + url)
            try:
                req = urllib.request.Request(url, headers={
                    'Connection': 'keep-alive',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
                })
                urlop = urllib.request.urlopen(req, timeout=1)
            except:
                bug_url |= {url}
                print("当前bug_url列表为%s", bug_url)
            if 'html' not in urlop.getheader('Content-Type'):
                continue
            data = urlop.read().decode('utf-8')
            # 循环所有re正则表达式对象
            # 千万注意正则表达式括号的中英文半角全角
            for rule_instance in self.rule_instance_list:
                linkre = rule_instance.my_compile
                column_value = linkre.findall(data)
                print('Name:%s, Value:%s' % (rule_instance.my_name, column_value))
                column_dict[rule_instance.my_name] = column_value
            print(column_dict)
            self.write_mysql(column_dict)  # 将得到的列名键对列名值的dict发送到写入数据库的方法

    # 创建一个链接队列，并将初始链接加入爬取队列
    def create_queue(self, start_url):
        queue = deque()
        queue.append(start_url)
        temp = self.queue_number
        self.queue_number += temp
        return queue

    # 这方法第一个参数传入正则表达式爬取的内容对应名字，第二个参数传入正则表达式字符串，返回一个RegularExpression类实例对象
    def create_re_rule(self, rule_name, re_string):
        instance = RegularExpression(re_string, rule_name)
        self.rule_instance_list.append(instance)
        return instance


class RegularExpression(object):
    # 建议实例Myname属性与数据库中列名一致，方便核对
    def __init__(self, my_re, my_name):
        self.my_re = my_re
        self.my_name = my_name
        self.my_compile = re.compile(self.my_re)
