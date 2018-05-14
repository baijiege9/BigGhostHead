# -*- coding: utf-8 -*-
# 哈工大的《基于行块分布函数的通用网页正文抽取算法》
# 约定：本文基于网页的不同行来进行统计，因此，假设网页内容是没有经过压缩的，就是网页有正常的换行的。
# 有些新闻网页，可能新闻的文本内容比较短，但其中嵌入一个视频文件，因此，我会给予视频较高的权重；
# 这同样适用于图片，这里有一个不足，应该是要根据图片显示的大小来决定权重的，但本文的方法未能实现这一点。
# 由于广告，导航这些非正文内容通常以超链接的方式出现，因此文本将给予超链接的文本权重为零。
# 这里假设正文的内容是连续的，中间不包含非正文的内容，因此实际上，提取正文内容，就是找出正文内容的开始和结束的位置。      
#步骤：
#   首先清除网页中CSS,Javascript,注释，Meta,Ins这些标签里面的内容，清除空白行。
#   计算每一个行的经过处理的数值（1）
#   计算上面得出的每行文本数的最大正子串的开始结束位置 
#其中第二步需要说明一下：
#    对于每一行，我们需要计算一个数值，这个数值的计算如下：
#    一个图片标签img，相当于出现长度为50字符的文本 （给予的权重），x1,
#    一个视频标签embed，相当于出现长度为1000字符的文本, x2
#    一行内所有链接的标签 a 的文本长度 x3 ,
#    其他标签的文本长度 x4
#    每行的数值 = 50 * x1其出现次数 + 1000 * x2其出现次数 + x4 – 8
# 	 说明， -8 因为我们要计算一个最大正子串，因此要减去一个正数，至于这个数应该多大，我想还是按经验来吧。 
import re

def remove_js_css (content):
    """ remove the the javascript and the stylesheet and the comment content (<script>....</script> and <style>....</style> <!-- xxx -->) """
    r = re.compile(r'''<script.*?</script>''',re.I|re.M|re.S)
    s = r.sub ('',content)
    r = re.compile(r'''<style.*?</style>''',re.I|re.M|re.S)
    s = r.sub ('', s)
    r = re.compile(r'''<!--.*?-->''', re.I|re.M|re.S)
    s = r.sub('',s)
    r = re.compile(r'''<meta.*?>''', re.I|re.M|re.S)
    s = r.sub('',s)
    r = re.compile(r'''<ins.*?</ins>''', re.I|re.M|re.S)
    s = r.sub('',s)
    return s

def remove_empty_line (content):
    """remove multi space """
    r = re.compile(r'''^\s+$''', re.M|re.S)
    s = r.sub ('', content)
    r = re.compile(r'''\n+''',re.M|re.S)
    s = r.sub('\n',s)
    return s

def remove_any_tag (s):
    s = re.sub(r'''<[^>]+>''','',s)
    return s.strip()

def remove_any_tag_but_a (s):
    text = re.findall (r'''<a[^r][^>]*>(.*?)</a>''',s,re.I|re.S|re.S)
    text_b = remove_any_tag (s)
    return len(''.join(text)),len(text_b)

def remove_image (s,n=50):
    image = 'a' * n
    r = re.compile (r'''<img.*?>''',re.I|re.M|re.S)
    s = r.sub(image,s)
    return s

def remove_video (s,n=1000):
    video = 'a' * n
    r = re.compile (r'''<embed.*?>''',re.I|re.M|re.S)
    s = r.sub(video,s)
    return s

def sum_max (values):
    cur_max = values[0]
    glo_max = -999999
    left,right = 0,0
    for index,value in enumerate (values):
        cur_max += value
        if (cur_max > glo_max) :
            glo_max = cur_max
            right = index
        elif (cur_max < 0):
            cur_max = 0

    for i in range(right, -1, -1):
        glo_max -= values[i]
        if abs(glo_max < 0.00001):
            left = i
            break
    return left,right+1

def method_1 (content, k=1):
    if not content:
        return None,None,None,None
    tmp = content.split('\n')
    group_value = []
    for i in range(0,len(tmp),k):
        group = '\n'.join(tmp[i:i+k])
        group = remove_image (group)
        group = remove_video (group)
        text_a,text_b= remove_any_tag_but_a (group)
        temp = (text_b - text_a) - 9
        group_value.append (temp)
    left,right = sum_max (group_value)
    return left,right, len('\n'.join(tmp[:left])), len ('\n'.join(tmp[:right]))

def extract (content):
    content = remove_empty_line(remove_js_css(content))
    left,right,x,y = method_1 (content)
    return '\n'.join(content.split('\n')[left:right])