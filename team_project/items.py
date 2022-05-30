# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Leo
class WeiXinItem(scrapy.Item):
    Title = scrapy.Field()          # 标题
    News_Time = scrapy.Field()      # 新闻发布时间
    Curr_Time = scrapy.Field()      # 当前爬取时间
    Info_url = scrapy.Field()       # 详情页url
    Page_Source = scrapy.Field()    # 新闻来源
    HTML = scrapy.Field()           # 详情页HTML
    Imag_content = scrapy.Field()   # 图片
    Imag_Urls = scrapy.Field()      # 图片url
    timearr = scrapy.Field()        # 时间记录

# fu
class SouhuItem(scrapy.Item):
    img_name = scrapy.Field()       # 图片来源网站
    html = scrapy.Field()           # 网站的html
    img_url = scrapy.Field()        # 图片所在网站的url
    img_src = scrapy.Field()        # 当前网站所有图片的url列表
    img_content = scrapy.Field()    # 当前网站所有的图片
    timearr = scrapy.Field()        # 时间记录

class hzItem(scrapy.Item):
    img_name = scrapy.Field()       # 图片来源网站
    html = scrapy.Field()           # 网站的html
    img_url = scrapy.Field()        # 图片所在网站的url
    img_src = scrapy.Field()        # 当前网站所有图片的url列表
    img_content = scrapy.Field()    # 当前网站所有的图片
    timearr = scrapy.Field()        # 时间记录

class qqItem(scrapy.Item):
    img_name = scrapy.Field()       # 图片来源网站
    html = scrapy.Field()           # 网站的html
    img_url = scrapy.Field()        # 图片所在网站的url
    img_src = scrapy.Field()        # 当前网站所有图片的url列表
    img_content = scrapy.Field()    # 当前网站所有的图片
    timearr = scrapy.Field()        # 时间记录

class zjolItem(scrapy.Item):
    img_name = scrapy.Field()       # 图片来源网站
    html = scrapy.Field()           # 网站的html
    img_url = scrapy.Field()        # 图片所在网站的url
    img_src = scrapy.Field()        # 当前网站所有图片的url列表
    img_content = scrapy.Field()    # 当前网站所有的图片
    timearr = scrapy.Field()        # 时间记录

# qian
class ChinaItem(scrapy.Item):
    img_name = scrapy.Field()  # 图片来源网站
    info_html = scrapy.Field()  # 新闻页html
    info_url = scrapy.Field()  # 新闻页url
    img_src = scrapy.Field()  # 图片url
    img_content = scrapy.Field()  # 图片字节数组
    timearr = scrapy.Field()  # 时间记录

class ChinayouthItem(scrapy.Item):
    img_name = scrapy.Field()  # 图片来源网站
    info_html = scrapy.Field()  # 新闻页html
    info_url = scrapy.Field()  # 新闻页url
    img_src = scrapy.Field()  # 图片url
    img_content = scrapy.Field()  # 图片字节数组
    timearr = scrapy.Field()  # 时间记录

class PeopleItem(scrapy.Item):
    img_name = scrapy.Field()  # 图片来源网站
    info_html = scrapy.Field()  # 新闻页html
    info_url = scrapy.Field()  # 新闻页url
    img_src = scrapy.Field()  # 图片url
    img_content = scrapy.Field()  # 图片字节数组
    timearr = scrapy.Field()  # 时间记录

class YangguangItem(scrapy.Item):
    img_name = scrapy.Field()  # 图片来源网站
    info_html = scrapy.Field()  # 新闻页html
    info_url = scrapy.Field()  # 新闻页url
    img_src = scrapy.Field()  # 图片url
    img_content = scrapy.Field()  # 图片字节数组
    timearr = scrapy.Field()  # 时间记录
