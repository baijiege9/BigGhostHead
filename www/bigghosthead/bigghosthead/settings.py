# -*- coding: utf-8 -*-

# Scrapy settings for bigghosthead project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bigghosthead'

SPIDER_MODULES = ['bigghosthead.spiders']
NEWSPIDER_MODULE = 'bigghosthead.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bigghosthead (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
   'Cookie': '__jda=122270672.587570459.1489142411.1498783000.1498787748.22; __jdu=587570459; TrackID=1grRavjSXuGgVAr8-AyORkUtVbSVyp6HlNXLOCj5ZlIEkfEiGuoDVyHR0sxWdzRzCye947-T5VNHjA91gzuXYZFAiHWefBNlR15ySYISqKhU; pinId=1i_e86gMUP8GeDFmU-aO0g; unpl=V2_ZzNtbRAAEBwmAUQGexoJDWICEwkSV0RGclpDXXseWFJjAxYIclRCFXMUR1NnG10UZgoZX0VcQhdFCEdkeBpdAWQCEFRHZ3MURQtGZHMpWAxhBxRcR1NLJUUPdmQHRxddOl5CXkNXRiV2C0dQexBeBmEzE21GVEYXdQlOUXwpF2tmThZURFNFFHAMTmR6KV8%3d; __jdv=122270672|e.firefoxchina.cn|t_220520384_|tuiguang|cfb8b83c12d9400ea16b6c48165f515d|1498783000435; user-key=d07c1d7e-a6db-4ef1-b44f-576149e1f1d8; cn=0; ipLoc-djd=1-72-2799-0; __jdc=122270672; 3AB9D23F7A4B3C9B=24CHWH7HXUBR3Q5CQDRTCXDQHPEJF7KMGQUT54PGJ3VY3DOG7NCU3DKHVLTZ4JLQ4OV74P2RZF6AW5C2LXVRGX2V6M',
   'Connection': 'keep-alive',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bigghosthead.middlewares.BigghostheadSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'bigghosthead.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
WEBSERVICE_ENABLED = True
WEBSERVICE_PORT = [6080,7030]
WEBSERVICE_HOST = "127.0.0.1"
WEBSERVICE_RESOURCES_BASR = {
	'scrapy.contrib.webservice.crawler.CrawlerResource': 1,
    'scrapy.contrib.webservice.enginestatus.EngineStatusResource': 1,
    'scrapy.contrib.webservice.stats.StatsResource': 1,
}
EXTENSIONS = {
	'scrapy_jsonrpc.webservice.WebService': 500,
}
JSONRPC_ENABLED = True
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bigghosthead.pipelines.BigghostheadPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#REDIS_URL = 'redis://woaiqiuxiaodong.top:6379'# 这个字段在solve也就是客户端使用
#FILTER_URL = None
#FILTER_HOST = 'localhost'
#FILTER_PORT = 6379
#FILTER_DB = 0
# REDIS_QUEUE_NAME = 'OneName'   # 如果不设置或者设置为None，则使用默认的，每个spider使用不同的去重队列和种子队列。如果设置了，则不同spider共用去重队列和种子队列

"""
    这是去重队列的Redis信息。
    原先的REDIS_HOST、REDIS_PORT只负责种子队列；由此种子队列和去重队列可以分布在不同的机器上。
"""