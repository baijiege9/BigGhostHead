import urllib.request
import time
import json
import asyncio

class Basic:
    def __init__(self):
        self.access_token = ""
        self.left_time = 0
        self.url_head = ""

    @asyncio.coroutine
    def first_get_access_token(self):
        appid = "wx3c3720856c6699fc"
        appsecret = "58054bd6695c432a3e909d7df935e0a3"
        post_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid, appsecret)
        url_resp = urllib.request.urlopen(post_url)
        url_head = url_resp.headers
        url_resp = json.loads(url_resp.read())
        self.accesstoken = url_resp['access_token']
        self.left_time = url_resp['expires_in']
        self.url_head = url_head

    @asyncio.coroutine
    def get_access_token(self):
        if self.left_time < 10:
            self.first_get_access_token()
        return self.accesstoken

    def get_urlopen_head(self):
        return self.url_head

    @asyncio.coroutine
    def run(self):
        while(True):
            if self.left_time > 10:
                time.sleep(2)
                self.left_time -= 2
            else:
                self.first_get_access_token()

def create(postData, access_token):
    post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
    if isinstance(postData, str):
        postData = postData.encode('utf-8')
    url_resp = urllib.request.urlopen(url=post_url, data=postData)
    data = url_resp.read()
    return data
        
#获取自定义菜单配置接口
def get_current_selfmenu_info(access_token):
    post_url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % access_token
    url_resp = urllib.request.urlopen(url=post_url)
    data = url_resp.read()
    return data

if __name__ == '__main__':
    post_json = """
    {
        "button": [
            {
                "name": "自定义菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "白睫哥博客",
                        "url": "http://www.baijiege.top/"
                    },
                    {
                        "type": "view",
                        "name": "白睫哥的github",
                        "url": "https://github.com/baijiege9"
                    },
                    {
                        "type": "view",
                        "name": "爬虫管理系统",
                        "url": "http://www.baijiege.top/spider/manage_bigghosthead"
                    }
                ]
            }
        ]
    }
    """
    access_token = Basic().get_access_token()
    #myMenu.delete(accessToken)
    create(post_json, access_token)
