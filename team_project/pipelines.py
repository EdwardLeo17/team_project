# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from team_project.items import WeiXinItem, SouhuItem, hzItem, qqItem, \
    zjolItem, ChinaItem, ChinayouthItem, PeopleItem, YangguangItem
from team_project.sava2Hbase import spider2save


class TeamProjectPipeline:
    def process_item(self, item, spider):
        # Leo
        if isinstance(item, WeiXinItem):
            # 微信爬虫数据处理
            print('*' * 80)
            print('WeiXin_Spider')
            print('*' * 80)
            print(item['Page_Source'])
            print(item['Title'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['Imag_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['Title'],
            #         Html='html',
            #         Info_Url=item['Info_Url'],
            #         Imag_contnet=item['Imag_content'],
            #         Imag_Urls=item['Imag_Urls'],
            #         createBy="Leo"
            #     )


        # fu
        elif isinstance(item, SouhuItem):
            # 搜狐爬虫数据处理
            print('*' * 80)
            print('Souhu_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['img_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['img_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, hzItem):
            # 杭州爬虫数据处理
            print('*' * 80)
            print('hz_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['img_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['img_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, qqItem):
            # QQ爬虫数据处理
            print('*' * 80)
            print('qq_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['img_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['img_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, zjolItem):
            # zjol爬虫数据处理
            print('*' * 80)
            print('zjol_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['img_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['img_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        # qian
        elif isinstance(item, ChinaItem):
            # 中国爬虫数据处理
            print('*' * 80)
            print('China_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['info_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['info_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, ChinayouthItem):
            # 青年爬虫数据处理
            print('*' * 80)
            print('Chinayouth_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['info_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['info_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, PeopleItem):
            # 人民爬虫数据处理
            print('*' * 80)
            print('People_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['info_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['info_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        elif isinstance(item, YangguangItem):
            # 阳光爬虫数据处理
            print('*' * 80)
            print('Yangguang_Spider')
            print('*' * 80)
            print(item['img_name'])
            print(item['info_url'])
            print('图片下载时间：', item['timearr'][1] - item['timearr'][0])
            print('截图时间：', item['timearr'][2] - item['timearr'][1])
            print(len(item['img_content']))
            print('\r' * 2)
            # # 发送数据
            # if len(item['img_content']) > 1:
            #     spider2save(
            #         Title=item['img_name'],
            #         Html='html',
            #         Info_Url=item['info_url'],
            #         Imag_contnet=item['img_content'],
            #         Imag_Urls=item['img_src'],
            #         createBy="Leo"
            #     )

        return item
