from io import BytesIO

import scrapy
from scrapy.linkextractors import LinkExtractor
from team_project import sava2Hbase
from team_project.items import zjolItem
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import requests
import time
import base64
from scrapy_redis.spiders import RedisSpider
from pyppeteer import launch
import asyncio

#启动splash

# 截图序号
global num
num = 0

# 记录层数
global level
level = 1

# 当前爬取层数
global now_level
now_level = 0

#外链解析中的链接采用键值对存储，链接作为key，层数作为values，可以通过控制values的上限控制其爬取层数
global url_dic
url_dic = {}

#存储图片url
global img_src_list
img_src_list = []

#存储图片字节数组
global img_content_list
img_content_list = []



script = """
                function main(splash, args)
                splash:go(args.url)
                local scroll_to = splash:jsfunc("window.scrollTo")
                scroll_to(0, 2800)
                splash:set_viewport_full()
                splash:wait(8)
                return {html=splash:html()}
                end 
 
        """



class ZjolSpider(RedisSpider):
    name = 'zjol'

    def start_requests(self):
        url = 'https://www.zjol.com.cn/'
        yield SplashRequest(url, self.parse,  endpoint='execute', args={'lua_source': script, 'url': url})

    # 负责截图的函数
    async def screenshot_main(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        src = await page.screenshot(fullPage=True)
        await browser.close()
        return src

    #截图保存
    # def pic_save(self, response):
    #     with open('浙江在线.png', 'wb') as f:
    #          f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        link = LinkExtractor('zjol.com.cn')
        links = link.extract_links(response)
        return links

        # 加到待爬取列表里
    def link_add(self, links):
        global level
        global url_dic
        for link in links:
            key = link.url
            url_dic[key] = level
        level = level + 1
        return url_dic


    def pic_find(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    def url_edit(self,pic):
        url =pic
        head = 'http'
        tag_url = 'zjol.com.cn'
        tag1 = 'static'
        if tag_url in url:
            if head in url:
                pic_url =url
            else:
                pic_url = 'http:'+url
        elif head in url:
            pic_url = url
        else:
            if tag1 in url:
                pic_url = 'https://' + url
            else:
                pic_url = 'https://img.zjol.com.cn/mlf/dzw' + url
        return pic_url

    def parse(self, response):
        global url_dic
        item, url_dic = self.url_parse(response)
        yield item
        for key, values in url_dic.items():
            url = key
            if (values == 1):
                url_dic[url] = 0
                yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'url': url})

    def url_parse(self, response):
        img_content_list = []
        img_src_list = []
        timearr = []
        pic_list = self.pic_find(response)
        item = zjolItem()
        item['img_name'] = 'souhu'
        item['img_url'] = response.url
        item['html'] = response

        st = time.time()
        timearr.append(st)
        for pic in pic_list:
            try:
                pic_src = pic['src']
            except Exception:
                continue

            if (pic_src == '' or pic_src == '//:0' or ('../' in pic_src)):
                continue
            src = self.url_edit(pic_src)
            img_src_list.append(src)
            # 获取图片响应
            try:
                pic_res = requests.get(src)
            except Exception:
                continue

            if pic_res.status_code == 200:
                pic_res.encoding = 'gbk'
            d = BytesIO(pic_res.content)
            data = []
            while True:
                t = d.read(1)
                if not t:
                    break
                data.append(t)
            data = sava2Hbase.jb2jb(data)
            img_content_list.append(data)
        t1 = time.time()
        timearr.append(t1)
        # 截图
        screenshot_src = asyncio.get_event_loop().run_until_complete(self.screenshot_main(response.url))
        d = BytesIO(screenshot_src)
        data = []
        while True:
            t = d.read(1)
            if not t:
                break
            data.append(t)
        data = sava2Hbase.jb2jb(data)
        img_content_list.append(data)
        t2 = time.time()
        timearr.append(t2)

        links = self.links_return(response)
        url_dic = self.link_add(links)

        # 图片字节数组列表
        item['img_content'] = img_content_list
        # 图片url列表
        item['img_src'] = img_src_list
        item['timearr'] = timearr

        return item, url_dic

