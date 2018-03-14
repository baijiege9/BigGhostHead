#!/usr/bin/env python3
# -*- coding: utf-8 -*-



' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

import markdown2

import hashlib

import urllib
from aiohttp import web
import xlrd

from coroweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError

from models import User, Comment, Blog, next_id, Students, Students_score, Spider
from config import configs
import xls_import
import receive
import access_token
import urllib.request

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret
new_access_token_instance = access_token.Basic()
new_access_token_instance.run()

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

def dict_handle(t):
    return t[1]

@asyncio.coroutine
def xls_import(route):
    data = xlrd.open_workbook('xls/%s'%route)
    table = data.sheets()[0]
    nrows = table.nrows # 获取行数
    ncols = table.ncols # 获取列数
    # 数据库字段名数组
    field_list = table.row_values(1)
    try:
        for nrow in range(3,nrows):# nrow: int
            temp_list = table.row_values(nrow)
            temp_dict = {}
            temp_dict['学号'] = temp_list[1]
            if temp_dict['学号'] == '':
                print('break')
                break 
            temp_dict['姓名'] = temp_list[2]
            for ncol in range(3,ncols):
                temp_dict[field_list[ncol]] = temp_list[ncol]
            print(temp_dict)
            student = Students(
                name = temp_dict['姓名'],
                student_number = temp_dict['学号'],
                school = '惠州城市职业学院',
                DZSWGL = temp_dict['电子商务概论'],
                SCYXSW = temp_dict['市场营销实务'],
                WYSJYY = temp_dict['网页设计语言'],
                DXSXLJKJY = temp_dict['大学生心理健康教育'],
                DXYY = temp_dict['大学英语'],
                TYYJK = temp_dict['体育与健康'],
                SXDDXYYFLJC = temp_dict['思想道德修养与法律基础'],
                PMSJ = temp_dict['平面设计'],
                DZSWYY = temp_dict['电子商务运营'],
                WYBJYMG = temp_dict['网页编辑与美工']
            )
            yield from student.save()
            # xls_import.analysis(student)
            temp_dict.pop('姓名')
            temp_dict.pop('学号')
            temp_list = [ 
                ('电子商务概论',temp_dict['电子商务概论']),
                ('市场营销实务',temp_dict['市场营销实务']),
                ('网页设计语言',temp_dict['网页设计语言']),
                ('大学生心理健康教育',temp_dict['大学生心理健康教育']),
                ('大学英语',temp_dict['大学英语']),
                ('体育与健康',temp_dict['体育与健康']),
                ('思想道德修养与法律基础',temp_dict['思想道德修养与法律基础']),
                ('平面设计',temp_dict['平面设计']),
                ('电子商务运营',temp_dict['电子商务运营']),
                ('网页编辑与美工',temp_dict['网页编辑与美工']),
            ] # 临时顺序排列列表
            temp_list = sorted(temp_list, key = dict_handle)
            student_score = Students_score(
                name = student.name,
                student_number = student.student_number,
                school = '惠州城市职业学院',
                best_kemu1 = temp_list[9][0],
                best_kemu2 = temp_list[8][0],
                best_kemu3 = temp_list[7][0],
                best_kemu4 = temp_list[6][0],
                best_kemu5 = temp_list[5][0],
                best_score1 = temp_list[9][1],
                best_score2 = temp_list[8][1],
                best_score3 = temp_list[7][1],
                best_score4 = temp_list[6][1],
                best_score5 = temp_list[5][1],
                bad_kemu1 = temp_list[0][0],
                bad_kemu2 = temp_list[1][0],
                bad_kemu3 = temp_list[2][0],
                bad_kemu4 = temp_list[3][0],
                bad_kemu5 = temp_list[4][0],
                bad_score1 = temp_list[0][1],
                bad_score2 = temp_list[1][1],
                bad_score3 = temp_list[2][1],
                bad_score4 = temp_list[3][1],
                bad_score5 = temp_list[4][1],
            )
            yield from student_score.save()
            logging.info('import out student:%s'%student)
        return 'OK'
    except:
        return '出事了'

@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
def index(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    page = Page(num,page_index)
    if num == 0:
        blogs = []
    else:
        blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }

@get('/blog/{id}')
def get_blog(id):
    blog = yield from Blog.find(id)
    comments = yield from Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }

@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }

@post('/api/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@get('/manage/')
def manage():
    return 'redirect:/manage/comments'

@get('/manage/comments')
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }

@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }

@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }

@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }

@get('/api/comments')
def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = yield from Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)

@post('/api/blogs/{id}/comments')
def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = yield from Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    yield from comment.save()
    return comment

@post('/api/comments/{id}/delete')
def api_delete_comments(id, request):
    check_admin(request)
    c = yield from Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    yield from c.remove()
    return dict(id=id)

@get('/api/users')
def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = yield from User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = yield from User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    yield from user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/blogs')
def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = yield from Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    return blog

@post('/api/blogs')
def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    yield from blog.save()
    return blog

@post('/api/blogs/{id}')
def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = yield from Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    yield from blog.update()
    return blog

@post('/api/blogs/{id}/delete')
def api_delete_blog(request, *, id):
    check_admin(request)
    blog = yield from Blog.find(id)
    yield from blog.remove()
    return dict(id=id)


# 
# 爬虫web端部分
# 
@get('/spider/manage_bigghosthead')
def spider_manage_bigghosthead(*, page='1'):
    return {
        '__template__': 'manage_bigghosthead.html',
        'page_index': get_page_index(page)
    }

@get('/spider/bigghosthead/{id}')
def get_spider(id):
    spider = yield from Spider.find(id)
    #crawling_speed
    #crawed_number
    return {
        '__template__': 'bigghosthead.html',
        'spider':spider
    }

@get('/blog/{id}')
def get_blog(id):
    blog = yield from Blog.find(id)
    comments = yield from Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }

@get('/spider/create_bigghosthead')
def spider_create_bigghosthead():
    return {
        '__template__': 'spider_edit.html',
        'id': '',
        'action': '/api/create_spider'
    }

@get('/api/crawed/number')
def get_crawed_number():
    test = 1
    return dict(number = test)

@get('/api/spider/bigghosthead')
def api_bigghosthead(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Spider.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, spiders=())
    spiders = yield from Spider.findAll( limit=(p.offset, p.limit))
    return dict(page=p, spiders=spiders)

@get('/api/spider/{id}')
def api_get_spider(*, id):
    spider = yield from Spider.find(id)
    return spider

@get('/api/start_spider/{id}')
def api_start_spider(*, request, id):
    check_admin(request)

@get('/api/stop_spider/{id}')
def api_stop_spider(*, request, id):
    check_admin(request)

@post('/api/create_spider')
def api_create_spider(request, *, spider_name, url, allowed_domains, spider_type, xpath_title, xpath_store, xpath_comment, xpath_text):
    check_admin(request)
    if not spider_name or not spider_name.strip():
        raise APIValueError('spider_name', 'spider_name cannot be empty.')
    if not url or not url.strip():
        raise APIValueError('url', 'url cannot be empty.')
    if not allowed_domains or not allowed_domains.strip():
        raise APIValueError('allowed_domains', 'allowed_domains cannot be empty.')
    if not spider_type or not spider_type.strip():
        raise APIValueError('spider_type', 'spider_type cannot be empty.')
    if not xpath_title or not xpath_title.strip():
        xpath_title = ''
    if not xpath_store or not xpath_store.strip():
        xpath_store = ''
    if not xpath_comment or not xpath_comment.strip():
        xpath_comment = ''
    if not xpath_text or not xpath_text.strip():
        xpath_text = ''
    spider = Spider(spider_name = spider_name.strip(), create_username = request.__user__.name, create_user_id = request.__user__.id, url = url.strip(), allowed_domains = allowed_domains.strip(), spider_type = spider_type.strip(), xpath_title = xpath_title.strip(), xpath_store = xpath_store.strip(), xpath_comment = xpath_comment.strip(), xpath_text = xpath_comment.strip())
    yield from spider.save()
    return spider

@post('/api/blogs')
def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    yield from blog.save()
    return blog

@post('/api/spider/{spider_id}/delete')
def api_spider_delete(*, spider_id):
    check_admin(request)    
    spider = yield from Spider.find(spider_id)
    yield from spider.remove()
    return '<script>window.location.href="/spider/manage_bigghosthead";</script>'

# 非blog内容，学生评价系统内容
@get('/api/students_score/{id}/delete')
def api_students_score_delete(*, id):
    students_score = yield from Students_score.find(id)
    yield from students_score.remove()
    return '<script>window.location.href="/teach_manage/students_score";</script>'

@get('/api/students/{id}/delete')
def api_students_delete(*, id):
    student = yield from Students.find(id)
    yield from student.remove()
    return '<script>window.location.href="/teach_manage/students_score";</script>'

@get('/teach_manage/class_students')
def teach_mange_class_students():
    return {
        '__template__' : 'teach_manage_class_students.html'
    }

@get('/api/students_score')
def api_students_score(*, page = '1'):
    page_index = get_page_index(page)
    num = yield from Students_score.findNumber('count(id)')
    print(num)
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, students_score=())
    students_score = yield from Students_score.findAll(limit=(p.offset, p.limit))
    print(students_score)
    return dict(page=p, students_score=students_score)

@get('/teach_manage')
def teach_manage():
    return {
        '__template__':'teach_manage.html',
    }

@get('/teach_manage/students_score')
def teach_manage_students_score(request, *, page='1'):
    page_index = get_page_index(page)
    num = yield from Students_score.findNumber('count(id)')
    page = Page(num, page_index)
    if num == 0:
        students_score = []
    else:
        print(page.offset)
        print(page.limit)
        students_score = yield from Students_score.findAll(limit=(page.offset, page.limit))
        print('___________________________________________________________________________')
    students = yield from Students.findAll()
    try:
        request.__user__.name
    except:
        return "请登录用户"
    # students_score = yield from Students_score.findAll()
    return {
        '__template__' : 'teach_mange_students_score.html',
        'teacher_name' : request.__user__.name,
        'students_score' : students_score,
        'page': page
    }

@post('/teach_manage/import')
def teach_manage_import(request):
    logging.info('____________________________________________________________')
    data = yield from request.post()
    xls = data['file']
    print(xls)
    filename = xls.filename
    xls_file = xls.file
    print(filename , xls.file)
    if xls.content_type != 'application/vnd.ms-excel' and xls.content_type != 'application/x-xls':
        return '不要搞事情，你这个是病毒吗？并不是xls表格'
    #print(request.post["SB"])
    f = open('xls/%s'%filename,'wb')
    f.write(xls_file.file.read())
    # f.write(xls_file)
    logging.info('____________________________________________________________')
    f.close()
    ok = yield from xls_import(filename)
    print(ok)
    return "成功保存%s表格<script>setTimeout(\"javascript:location.href=\'/teach_manage/students_score\'\", 999); </script>"%filename

@get('/teach_manage/curriculum')
def teach_manage_curriculum():
    return {
        '__template__' : 'teach_manage_curriculum.html'
    }

@get('/teach_manage/student_organizations')
def teach_manage_student_organizations():
    return {
        '__template__' : 'teach_manage_student_organizations.html'
    }

@get('/teach_manage/social practice')
def teach_manage_social_practice():
    return {
        '__template__' : 'teach_manage_social_practice.html'
    }

@get('/teach_manage/graduation design')
def teach_manage_graduation_design():
    return {
        '__template__' : 'teach_manage_graduation_design.html'
    }

@get('/teach_manage/activities')
def teach_manage_activities():
    return {
        '__template__' : 'teach_manage_activities.html'
    }

@get('/teach_manage/life')
def teach_manage_life():
    temp_body = "<xml><ToUserName><![CDATA[123321]]></ToUserName><FromUserName><![CDATA[321423]]></FromUserName><CreateTime>1234567890</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[hello,world!]]></Content></xml>"
    response = web.Response(body = temp_body, content_type = 'text/html')
    return response

#Wecat token
@get('/weixin_token')
def weixin_token(request, *, signature, timestamp, nonce, echostr):
    print("signature=",signature,"timestamp=",timestamp,"nonce=",nonce,"echostr=",echostr)
    token = "bigghosthead"
    list = [token.encode("utf8"), timestamp.encode("utf8"), nonce.encode("utf8")]
    list.sort()
    sha1 = hashlib.sha1()
    sha1.update(list[0])
    sha1.update(list[1])
    sha1.update(list[2])
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return echostr
    else:
        return ""

@get('/jiao_zuo_ye1')
def jiaozuoye(request):
    baidu_response = urllib.request.urlopen('http://www.baidu.com')
    baidu_html = baidu_response.read()
    baidu_response_headers = str(baidu_response.headers)
    new_access_token_instance = access_token.Basic()
    new_access_token = new_access_token_instance.get_access_token()
    new_access_token_headers = str(new_access_token_instance.get_urlopen_head())
    # string = "百度响应头头:"+baidu_response_headers+"\n access_token响应头"+new_access_token_headers+"\n access_token:"+new_access_token
    string = "百度响应头" + baidu_response_headers
    return string
""" 
    @get('rm_qingkong.html')
def qingkongcaidan(request):
    new_access_token_instance = access_token.Basic()
    new_access_token = new_access_token_instance.get_access_token()
    url
"""
@get('/jiao_zuo_ye2')
def jiaozuoye2(request):
    baidu_response = urllib.request.urlopen('http://www.baidu.com')
    baidu_html = baidu_response.read()
    baidu_response_headers = str(baidu_response.headers)
    new_access_token_instance = access_token.Basic()
    new_access_token = new_access_token_instance.get_access_token()
    new_access_token_headers = str(new_access_token_instance.get_urlopen_head())
    # string = "百度响应头头:"+baidu_response_headers+"\n access_token响应头"+new_access_token_headers+"\n access_token:"+new_access_token
    string = "access_token:" + new_access_token
    return {
        '__template__' : 'jiaozuoye.html',
        'zuoye' : string
    }

@post('/jiao_zuo_ye2')
def post_caidan(request):
    data = yield from request.post()
    name = data['name']
    url = data['url']
    first_json = """
    {
        "button": [
            {
                "name": "自定义菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "%s",
                        "url": "%s"
                    }
                ]
            }
        ]
    }
    """
    post_json = first_json%(name, url)
    reponse =  yield from access_token.create(post_json, new_access_token)
    return reponse

@post('/weixin_token')
def weixin_post(request):
    b_data = yield from request.read()
    data = yield from request.text()
    #data = post_data['data']
    rec_msg = receive.parse_xml(data)
    try:
        if isinstance(rec_msg, receive.Msg) and rec_msg.msg_type == 'text':
            name = rec_msg.Content
            students_score = yield from Students_score.findAll('name=?', [name])
            from_user = rec_msg.from_user_name
            to_user = rec_msg.to_user_name
            content = "students_name:" + students_score[0].name + "\nstudents_number："+ students_score[0].student_number + "\nbest_kemu1:" + students_score[0].best_kemu1 + "\nbest_score1:"+students_score[0].best_score1  + "\nbest_kemu2:" + students_score[0].best_kemu2 + "\nbest_score2:"+students_score[0].best_score2  + "\nbest_kemu3:" + students_score[0].best_kemu3 + "\nbest_score3:"+students_score[0].best_score3
            create_time = int(time.time())
            return {
                '__template__' : 'weixin.html',
                'ToUserName' : from_user,
                'FromUserName' : to_user,
                'CreateTime' : create_time,
                'Content' : content
            }
    except:
        from_user = rec_msg.from_user_name
        to_user = rec_msg.to_user_name
        create_time = int(time.time())
        return {
            '__template__' : 'weixin.html',
            'ToUserName' : from_user,
            'FromUserName' : to_user,
            'CreateTime' : create_time,
            'Content' : '你查询的名字不在数据库中~'
        }

@get('/curl_create_menu')
def ajax_get(request):
    return {
        '__template__' : 'ajax.html'
    }

@get('/graduation')
def graduation(request):
    return {
        '__template__' : 'graduation.html'
    }


@get('/graduation2')
def graduation2(request):
    return {
        '__template__' : 'graduation2.html'
    }