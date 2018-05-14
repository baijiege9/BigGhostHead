# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from models import User, Comment, Blog, next_id, Students, Students_score, Spider, Jd_comment, Product
#sys.setdefaultencoding('utf8')

class BigghostheadPipeline(object):
    def process_item(self, item, spider):
        #print(item)
        #conn = mysql.connector.connect(user = 'root', passwd = 'root',database = 'bigghosthead')
        #cursor = conn.cursor()
        #try:
         #   item['title']
         #   item['title'] = item['title']
          #  item['productId'] = item['productId']
         #   item['store'] = item['store']
            #cursor.execute('insert into product(product, productId, store)values (%s,%s,%s)',[item['title'], item['productId'],item['store']])
            #conn.commit()
            #conn.close()
         #   product = Product(product = item['title'], productId = item['productId'], store = item['store'])
         #   product.save()
         #   print("保存一条数据成功")
       # except:
          #  item['comment']
        #    item['comment'] = item['comment']
         #   item['productId'] = item['productId']
            #cursor.execute('insert into comment(comment, productId)values (%s,%s)',[item['comment'], item['productId']])
            #conn.commit()
            #conn.close()
         #   jd_comment = Jd_comment(productId = item['productId'], comment = item['comment'])
          #  jd_comment.save()
          #  print("保存一条数据也成功")
        return item
