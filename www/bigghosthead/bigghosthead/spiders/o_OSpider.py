#　-*- coding:utf-8 -*-
import datetime
from . import configclass
import re
import json
import scrapy
from . import web_text
# 抽取正文的模块
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.utils.url import urljoin_rfc

from bigghosthead.items import BigghostheadItem
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

config = configclass.Config()
class o_Ospder(Spider):
    name = "o_Ospider"
    def __init__(self, **kw):
        url = kw.get('url') or kw.get('domain')
        self.url = url
        self.allowed_domains = kw.get('allowed_domains')
        self.spider_type = kw.get('spider_type')
        self.xpath_title = kw.get('xpath_title','')
        self.xpath_store = kw.get('xpath_store','')
        self.xpath_comment = kw.get('xpath_comment','')
        self.xpath_text = kw.get('xpath_text','')
        self.xpath_keywords = kw.get('xpath_keywords','')

    def start_requests(self):
        if self.spider_type == "JD":
            return [Request(self.url, callback=self.jd_parse, dont_filter=True)]
        if self.spider_type == "normal_blog":
            return [Request(self.url, callback=self.normal_blog_parse, dont_filter=True)]
        if self.spider_type == "normal_shop":
            return [Request(self.url, callback=self.normal_shop_parse, dont_filter=True)]

    def jd_parse(self, response):
        item = BigghostheadItem()
        sites = response.selector.xpath('//a/@href')
        for site in sites:
            print(site.extract())
            try:
                pass
                yield scrapy.Request(site.extract(), callback = self.jd_parse, meta = {'http-equiv':"Content-Type", 'content':"text/html; charset=utf-8"})# 非绝对路径的那些不合法路径
            except:
                pass
                full_url = response.urljoin(site.extract())
                yield scrapy.Request(full_url, callback = self.jd_parse)
        if 'J-hove-wrap EDropdown fr' in response.text: # 经过验证，class = J-hove-wrap EDropdown fr 只会存在于京东的商品详情页面，而不会出现在首页商铺页面。
            # 充填xpath语法参数
            re_id = re.compile('https://item.jd.com/(\d+?).html')
            productId = re_id.findall(response.url)[0]
            comment_url = "https://sclub.jd.com/comment/productPageComments.action?productId="+ productId + "&score=0&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1"
            yield scrapy.Request(comment_url, callback = self.parse_comment)
            item['productId'] = productId
            if self.xpath_title != '':
                item['title'] = response.xpath(
                        self.xpath_title
                    ).extract()[0]
            if self.xpath_store != '':
                item['store'] = response.xpath(
                        self.xpath_store
                    ).extract()[0]
            if self.xpath_comment  != '':
                item['comment'] = response.xpath(
                        self.xpath_comment
                    ).extract()
            if self.xpath_text  != '':
                item['text'] = response.xpath(
                        self.xpath_text
                    ).extract()
        yield item

    def parse_comment(self, response):
        json_data = json.loads(response.text)
        for cd in json_data['comments']:
            item = BigghostheadItem()
            item['comment'] = cd['content']
            item['productId'] = cd['referenceId']
            yield item
        if not json_data['comments']:
            return# 如果当前页数评论api的json中没有评论了，那么结束    
        re_page = re.compile('page=(\d+?)')
        page = re_page.findall(response.url)[0]
        a = 'page='+page
        b = 'page='+str(int(page)+1)
        next_comment_url = response.url.replace(a,b)
        yield scrapy.Request(next_comment_url, callback = self.parse_comment)