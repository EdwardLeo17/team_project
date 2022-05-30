import scrapy
from team_project.items import PeopleItem
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import requests
from team_project import sava2Hbase
from copy import deepcopy
import asyncio
from pyppeteer import launch
from scrapy_redis.spiders import RedisSpider
import time

class peopleSpider(RedisSpider):
    name = 'people'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://people.com.cn/']

    # 负责截图
    async def screenshot_main(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        src = await page.screenshot(fullPage=True)
        await browser.close()
        return src

    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        link = LinkExtractor()
        links = link.extract_links(response)
        for link in links:
            item = PeopleItem()
            item['info_url'] = link.url
            yield scrapy.Request(link.url, callback=self.parse_item ,meta={'Item': deepcopy(item)})

    def parse_item(self, response):
        item = response.meta['Item']
        item['img_name'] = 'people'
        item['info_html'] = response.text
        soup = BeautifulSoup(response.text, 'html.parser')
        pic_list = soup.find_all('img')

        img_content = []
        img_srcs = []
        timearr = []

        st = time.time()
        timearr.append(st)
        for pic in pic_list:
            pic_src = pic['src']
            img_src = 'http://www.people.com.cn' + pic_src

            try:
                response = requests.get(img_src,verify=False)
            except Exception:
                pass
            else:
                img_srcs.append(img_src)    # 能正常访问的才会添加进去
                if response.status_code == 200:
                    response.encoding = 'gbk'
                d = sava2Hbase.BytesIO(response.content)
                data = []
                while True:
                    t = d.read(1)
                    if not t:
                        break
                    data.append(t)
                data = sava2Hbase.jb2jb(data)
                img_content.append(data)
        t1 = time.time()
        timearr.append(t1)

        # 截图
        try:
            screenshot_src = asyncio.get_event_loop().run_until_complete(self.screenshot_main(item['info_url']))
        except Exception:
            # print('截图失败！')
            timearr.append(0)
        else:
            # 转换截图为字节数组
            d = sava2Hbase.BytesIO(screenshot_src)
            data = []
            while True:
                t = d.read(1)
                if not t:
                    break
                data.append(t)
            data = sava2Hbase.jb2jb(data)
            img_content.append(data)
            t2 = time.time()
            timearr.append(t2)

        item['img_src'] = img_srcs
        item['img_content'] = img_content
        item['timearr'] = timearr

        yield item