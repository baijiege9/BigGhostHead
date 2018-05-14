# -*- coding: utf-8 -*-
from scrapy.item import Item, Field

class BigghostheadItem(Item):
    # 电商网站的fields
    productId = Field()
    title = Field()# 商品
    store = Field()# 店铺
    #新闻博客的fields
    text = Field()# 文本
    keywords = Field()# 关键词
    comment = Field()
    productId = Field()