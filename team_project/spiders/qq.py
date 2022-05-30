from io import BytesIO

import requests
import scrapy
from team_project.items import qqItem
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from team_project import sava2Hbase
import time
import base64
from scrapy_redis.spiders import RedisSpider
from pyppeteer import launch
import asyncio


#截图序号
global num
num = 0

#记录层数
global level
level = 1

#当前爬取层数
global now_level
now_level = 1

#外链解析中的链接采用键值对存储，链接作为key，层数作为values，可以通过控制values的上限控制其爬取层数
global url_dic
url_dic = []

#存储图片url
global img_src_list
img_src_list=[]

#存储图片字节数组
global img_content_list
img_content_list=[]


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
#截图脚本
# script_png = """
#                 function main(splash, args)
#                 splash:go(splash.args.url)
#                 splash:set_viewport_size(1500, 10000)
#                 local scroll_to = splash:jsfunc("window.scrollTo")
#                 scroll_to(0, 2800)
#                 splash:wait(8)
#                 return {png=splash:png()}
#                 end
#                 """
class QqSpider(RedisSpider):
    name = 'qq'
    #start_urls = ['https://www.qq.com/']

    def start_requests(self):
        url = 'https://www.qq.com/'
        yield scrapy.Request(url, self.parse)
        #yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})

    # 负责截图的函数
    async def screenshot_main(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        src = await page.screenshot(fullPage=True)
        await browser.close()
        return src

    # def pic_save(self, response):
    #     global num
    #     num = num + 1
    #     fname = 'qq' + str(num) + '.png'
    #     with open(fname, 'wb') as f:
    #          f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        link = LinkExtractor("qq.com")
        links = link.extract_links(response)

        return links

    #找到所有img标签
    def pic_find(self,response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    #加到待爬取列表里
    def link_add(self, links):
        global level
        global url_dic
        for link in links:
            key = link.url
            url_dic.append(key)
        #level = level + 1
        return url_dic

    def url_edit(self, pic_src):
        head = 'http'
        if head in pic_src:
            pic_url = pic_src
        else:
            pic_url = 'http:' + pic_src
        return pic_url

    def parse(self, response):
        global url_dic

        # 循环爬取部分
        links = self.links_return(response)
        url_dic = self.link_add(links)

        for url in url_dic:
            item = qqItem()
            item['img_name'] = 'qq'
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.url_parse)

    def url_parse(self, response):
        item = response.meta['item']
        # 当前页面图片字节数组列表
        img_content_list = []
        # 当前页面图片src
        img_src_list = []
        timearr = []

        pic_list = self.pic_find(response)

        if (response.url == "https://www.qq.com/"):
            item['img_url'] = response.url
            item['html'] = response
        else:
            item = response.meta['item']
            item['img_url'] = response.url
            item['html'] = response

        st = time.time()
        timearr.append(st)
        for pic in pic_list:
            try:
                pic_src = pic['src']
            except Exception:
                continue

            if (pic_src == '' or ('./' in pic_src)):
                continue
            src = self.url_edit(pic_src)
            img_src_list.append(src)

            # 获取图片响应
            try:
                pic_res = requests.get(src)
            except Exception:
                print('Error Url:', src)
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

        # 图片字节数组列表
        item['img_content'] = img_content_list
        # 图片url列表
        item['img_src'] = img_src_list
        item['timearr'] = timearr

        yield item
