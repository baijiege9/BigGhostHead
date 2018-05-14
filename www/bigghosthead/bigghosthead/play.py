#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *

import ConfigClass
import sys
import os
config = ConfigClass.Config()

class  WidgetsSimple:
    def __init__(self):
        window = Tk()
        window.title("大鬼头爬虫GUI")
        frame1 = Frame(window)
        frame2 = Frame(window)
        frame3 = Frame(window)
        self.frame1 = frame1
        self.frame2 = frame2
        self.frame3 = frame3
        frame1.pack() # 块位置
        self.v1 = IntVar()
        self.xpath_title = StringVar()
        self.xpath_store = StringVar()
        self.xpath_comment = StringVar()
        self.start_url = StringVar()
        self.allowed_domains = StringVar()
        label_one = Label(frame1, text = "爬取类型：")
        rbo_o = Radiobutton(frame1, text = "爬取电商网站", variable = self.v1, value = 1, command = self.processRaidobutton)
        rbblog = Radiobutton(frame1, text="爬取资讯网站", variable = self.v1, value = 2, command = self.processRaidobutton)
        label_two = Label(frame1, text = "start_url：")
        EntryUrl = Entry(self.frame1, textvariable = self.start_url)
        EntryUrl.grid(row = 2, column = 2)
        label = Label(frame1, text = "限定域名（可选）")
        label.grid(row = 3, column = 1)
        ENtryAllowed_domains = Entry(self.frame1, textvariable = self.allowed_domains)
        ENtryAllowed_domains.grid(row = 3, column = 2)
        label_two.grid(row = 2, column = 1)
        label_one.grid(row = 1, column = 1)
        rbo_o.grid(row = 1, column = 2)
        rbblog.grid(row = 1, column = 3)
        window.mainloop()

    def processRaidobutton(self):
        if self.v1.get() == 1:
            self.frame2.pack()
            self.frame3.pack_forget()
            label_two = Label(self.frame2, text = "商品名(xpath表达式)：")
            label_two.grid(row = 1, column = 1)
            EntryTitle = Entry(self.frame2, textvariable = self.xpath_title)
            EntryTitle.grid(row = 1, column = 2)
            label_three = Label(self.frame2, text = "店铺名(xpath表达式)：")
            label_three.grid(row = 2, column = 1)
            EntryStore = Entry(self.frame2, textvariable = self.xpath_store)
            EntryStore.grid(row = 2, column = 2)
            label_four = Label(self.frame2, text = "商品评价(xpath表达式)：")
            label_four.grid(row = 3, column = 1)
            EntryComment = Entry(self.frame2, textvariable = self.xpath_comment)
            EntryComment.grid(row = 3, column = 2)
            Button(self.frame2 , text = "保存配置", command = self.save).grid(row = 4, column = 1)
            Button(self.frame2 , text = "开启爬虫", command = self.start_o2o).grid(row = 4, column = 2)
        elif self.v1.get() == 2:
            self.frame2.pack_forget()
            self.frame3.pack()
            Button(self.frame3 , text = "开启爬虫", command = self.start_blog).grid(row = 4, column = 1)
        else:
            pass

    def start_blog(self):
    	print("start_blog")
        os.system("python wrBlog.py")

    def start_o2o(self):
    	os.system("scrapy crawl o_Ospider")

    def save(self):
    	pass
WidgetsSimple()
# 进入消息循环
