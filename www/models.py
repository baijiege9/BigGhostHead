#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''



import time, uuid
import sys
sys.path.append("..")
sys.path.append("..")

from orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)
    photo = StringField(ddl = 'varchar(500)')

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Students(Model):
    __table__ = 'students'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    student_number = StringField(ddl='varchar(50)')
    school = StringField(ddl='varchar(50)')
    DZSWGL = StringField(ddl='varchar(50)', default = '')
    SCYXSW = StringField(ddl='varchar(50)', default = '')
    WYSJYY = StringField(ddl='varchar(50)', default = '')
    DXSXLJKJY = StringField(ddl='varchar(50)', default = '')
    DXYY = StringField(ddl='varchar(50)', default = '')
    TYYJK = StringField(ddl='varchar(50)', default = '')
    SXDDXYYFLJC = StringField(ddl='varchar(50)', default = '')
    PMSJ = StringField(ddl='varchar(50)', default = '')
    DZSWYY = StringField(ddl='varchar(50)', default = '')
    WYBJYMG = StringField(ddl='varchar(50)', default = '')

class Students_score(Model):
    __table__ = 'students_score'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    student_number = StringField(ddl='varchar(50)')
    school = StringField(ddl='varchar(50)')
    best_kemu1 = StringField(ddl='varchar(50)')
    best_kemu2 = StringField(ddl='varchar(50)')
    best_kemu3 = StringField(ddl='varchar(50)')
    best_kemu4 = StringField(ddl='varchar(50)')
    best_kemu5 = StringField(ddl='varchar(50)')    
    best_score1 = StringField(ddl='varchar(50)', default = '')
    best_score2 = StringField(ddl='varchar(50)', default = '')
    best_score3 = StringField(ddl='varchar(50)', default = '')
    best_score4 = StringField(ddl='varchar(50)', default = '')
    best_score5 = StringField(ddl='varchar(50)', default = '')
    bad_kemu1 = StringField(ddl='varchar(50)')
    bad_kemu2 = StringField(ddl='varchar(50)')
    bad_kemu3 = StringField(ddl='varchar(50)')
    bad_kemu4 = StringField(ddl='varchar(50)')
    bad_kemu5 = StringField(ddl='varchar(50)')
    bad_score1 = StringField(ddl='varchar(50)', default = '')
    bad_score2 = StringField(ddl='varchar(50)', default = '')
    bad_score3 = StringField(ddl='varchar(50)', default = '')
    bad_score4 = StringField(ddl='varchar(50)', default = '')
    bad_score5 = StringField(ddl='varchar(50)', default = '')

# 爬虫
class Spider(Model):
    __table__ = 'spider'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    spider_name = StringField(ddl='varchar(50)')
    create_username = StringField(ddl='varchar(50)')
    create_user_id = StringField(ddl='varchar(50)')
    url = StringField(ddl='varchar(50)')
    allowed_domains = StringField(ddl='varchar(50)', default = '')
    spider_type = StringField(ddl='varchar(50)', default = '')
    xpath_title = StringField(ddl='varchar(50)', default = '')
    xpath_store = StringField(ddl='varchar(50)', default = '')
    xpath_comment = StringField(ddl='varchar(50)', default = '')
    xpath_text = StringField(ddl='varchar(50)', default = '')
'''
class Jd_comment(Model):
    __table__ = 'comment'

    productId = StringField(ddl='varchar(50)')
    comment = StringField(ddl='varchar(500)')

class Product(Model):
    __table__ = "product"

    product = StringField(ddl='varchar(500)')
    productId = StringField(ddl='varchar(50)')
    store = StringField(ddl='varchar(50)')'''


class Langem(Model):
    __table__ = 'langem'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    content = TextField()
    create_time = FloatField(default=time.time)
    title = StringField(ddl='varchar(50)', default = '')
