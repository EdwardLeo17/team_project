import scrapy
import json
import time
import requests
import asyncio
import sava2Hbase
from io import BytesIO
from pyppeteer import launch
from copy import deepcopy
from team_project.items import WeiXinItem
from scrapy_redis.spiders import RedisSpider

# 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5ODMzMDMyMw==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=MjM4MzU3NjU0Mw%3D%3D&key=&pass_ticket=wPj%2Fx0F3VrFWGG1QMTqfoDX1tGT7IzytXl0Gmz078l7p8g77HFE9pvNWLGf9JZq8&wxtoken=&appmsg_token=1167_HZ4aM6EN%252F1mdbCP7UVoo0d2RVcOMVPOzmsHpQA~~&x5=0&f=json'

class GzhSpider(RedisSpider):
    # 三个参数 __biz offset key
    content_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={}&offset={}&f=json&uin=MjM4MzU3NjU0Mw%3D%3D&key={}' # 大号 MjM4MzU3NjU0Mw%3D%3D  小号 MTE2Mjg5NjE1Nw%3D%3D
    NF_key = '06ab2b7f444daabf2986900dd64b2f7f8bca0d996d634c520cdbbb11a1ce00de5b338bd910f217eb91bd18231cea8bad42766d22ad2dfd6f810dc771e35521d2a6bb13593791bc6d4a718434311eb629e04e4e25bde3fa912004f54630e4858ed5971eccd01131dc6353de5b8daa1e40487ba441d242b6616a474eb0c69f8135'
    RW_KEY = '3919d66174dfaf320ae18d2417a8239fe0035a2892b081ae785619f3f7f85a965551639cffbda7026979d71bd59f24fa0f45dbca5ac63b8edfd0f4f31caf072f543d33a8688b21fa8d965ca03c2d8346b66435601997e2d40efd78f0da72e306fa33c11b82c361a9f423df479a2e20313108f9e808743f9480f3f26e4500f686'
    XZK_KEY = '3919d66174dfaf32c47268151ec73cfd82686bc3c6ce667387d93614733f553c4db02c9e59797087b664ecc2909e16cd80e924a46839948ef7501a66a83b49f0de5692952ca99277528b2b122b023f360b360a15d531a7309962bb6f1e8604bce90b8e35fe0ed73b537524c7c687ae528e73b6a0b17372189f9adea6bc4d7fa9'
    name = 'GZH'
    allowed_domains = ['weixin.com', 'mp.weixin.qq.com']
    start_urls = [content_url.format('Njk5MTE1', 0, NF_key)]
    # 设置爬取范围
    page_domain = 10

    # 负责截图的函数
    async def screenshot_main(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        src = await page.screenshot(fullPage=True)
        await browser.close()
        return src

    def start_requests(self):
        # redis_serve = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        # redis_serve.lpush('GZH:start_urls', self.content_url.format('Njk5MTE1', 0, self.NF_key))

        # NF翻页处理
        for i in range(self.page_domain):
            next_page = self.content_url.format('Njk5MTE1', str(i * 10), self.NF_key)
            yield scrapy.Request(next_page,callback=self.parse)
        # RW翻页处理
        for i in range(self.page_domain):
            next_page = self.content_url.format('MjEwMzA5NTcyMQ==', str(i * 10), self.RW_KEY)
            yield scrapy.Request(next_page,callback=self.parse)
        # XZK翻页处理
        for i in range(self.page_domain):
            next_page = self.content_url.format('MjM5ODMzMDMyMw==', str(i * 10), self.XZK_KEY)
            yield scrapy.Request(next_page,callback=self.parse)

    # 用于解析列表页
    def parse(self, response):
        # 解析新闻列表
        info_dic = json.loads(response.text)
        try:
            info_list = json.loads(info_dic['general_msg_list'])['list']
        except Exception:
            print('url失效，请重新获取')
        else:
            for info in info_list:
                # 解析第一级列表
                app_msg_ext_info = info['app_msg_ext_info']
                # 标题 (不一样)
                Title = app_msg_ext_info['title']
                # 新闻时间 (一样的)
                timeStamp = info['comm_msg_info']['datetime']
                timeArray = time.localtime(timeStamp)
                news_Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                # 爬取时间 (一样的)
                curr_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
                # 新闻url (不一样)
                info_url = app_msg_ext_info['content_url']

                Item = WeiXinItem(Title=Title, News_Time=news_Time, Curr_Time=curr_Time, Info_url=info_url)
                try:
                    yield scrapy.Request(
                        url=info_url,
                        callback=self.info_parse,
                        meta={'Item': deepcopy(Item)},
                    )
                except Exception:
                    print('*'*80)
                    print('解析新闻页url失败！！！')
                    print(info_url)
                    print('*' * 80)

                # 解析第二级列表
                multi_app_msg_item_list = app_msg_ext_info['multi_app_msg_item_list']
                for muti_msg in multi_app_msg_item_list:
                    # 标题 (不一样)
                    Title = muti_msg['title']
                    # 新闻url
                    info_url = muti_msg['content_url']

                    Item = WeiXinItem(Title=Title, News_Time=news_Time, Curr_Time=curr_Time, Info_url=info_url)
                    # print(Item)
                    yield scrapy.Request(
                        url=info_url,
                        callback=self.info_parse,
                        meta={'Item': deepcopy(Item)},
                    )

    # 新闻内容页解析
    def info_parse(self, response):
        Item = response.meta['Item']
        # HTML
        Item['HTML'] = response.text
        # 新闻来源公众号
        page_source = response.xpath('//a[@class="wx_tap_link js_wx_tap_highlight weui-wa-hotarea"]/text()').get()
        if page_source:
            Item['Page_Source'] = page_source.strip()
        else:
            Item['Page_Source'] = ''
        # 图片url
        Item['Imag_Urls'] = response.xpath('//img/@data-src').getall()

        # 图片保存
        img_content = []
        timearr = []

        st = time.time()
        timearr.append(st)
        for img_url in Item['Imag_Urls']:
            res = requests.get(img_url)
            # 转换为字节数组
            if res.status_code == 200:
                res.encoding = 'gbk'
            d = BytesIO(res.content)
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
        screenshot_src = asyncio.get_event_loop().run_until_complete(self.screenshot_main(Item['Info_url']))
        # 转换截图为字节数组
        d = BytesIO(screenshot_src)
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

        Item['Imag_content'] = img_content
        Item['timearr'] = timearr

        yield Item
