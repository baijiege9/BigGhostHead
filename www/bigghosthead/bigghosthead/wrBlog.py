#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import web_text
import codecs

for filename in os.listdir('testhtml'):
    try:
        with codecs.open('testhtml/'+filename, 'r', 'utf-8') as f:
            data = web_text.extract(f.read())
        with codecs.open('shuchu/'+filename, 'w', 'utf-8') as w:
            w.write(data)
            print("当前从testhtml/"+filename+"提取到"+"shuchu/"+filename+"成功")
    except:
        print("当前从testhtml/"+filename+"提取到"+"shuchu/"+filename+"失败")
