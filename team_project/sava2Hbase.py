import datetime
import logging
import os
import sys
import time
import requests

from io import BytesIO


# python bytes（0，256），java byte（-127，128）
def jb2jb(byte_arr):
    """
    [-255,256) 映射 到 [-128 ~ 127]
    @param byte_arr:
    @return: byte_arr
    """
    new_list = []
    for i in byte_arr:
        a = int.from_bytes(i, byteorder=sys.byteorder, signed=True)
        if a < -128:
            new_list.append(a + 256)
        elif a > 127:
            new_list.append(a - 256)
        else:
            new_list.append(a)
    return new_list


def pb2str(byte_arr, encoding="utf-8"):
    """
    python字节码转str
    :return:
    """
    return bytes(byte_arr).decode(encoding)


def img2Bytes(path):
    res = []
    with open(path, 'rb') as f:
        size = os.path.getsize(path)
        # print(size)
        while True:
            # 每次读取一个字符
            t = f.read(1)
            # 如果没有读到数据，跳出循环
            if not t:
                break
            val = int().from_bytes(t, byteorder=sys.byteorder, signed=True)
            res.append(val)
        f.close()
    return res


def bytes2Img(bytes, path):
    with open(path, 'wb') as f:
        for i in range(len(bytes)):
            val = int(bytes[i]).to_bytes(length=1, byteorder=sys.byteorder, signed=True)
            # print(val)
            f.write(val)
        f.close()


def url2save(Info_Url, url_):
    response = requests.get(url_)
    if response.status_code == 200:
        response.encoding = 'gbk'
    d = BytesIO(response.content)
    data = []
    while True:
        t = d.read(1)
        if not t:
            break
        data.append(t)
    data = jb2jb(data)
    data_list = list()
    data_list.append(data)
    print(data)
    sava('cqj', Info_Url, data_list, 'cqj', remark='halo哈喽')


def urlList2save(Info_Url, Imag_Urls, Title=None):
    data_list = list()
    for url_ in Imag_Urls:
        response = requests.get(url_)
        if response.status_code == 200:
            response.encoding = 'gbk'
        d = BytesIO(response.content)
        data = []
        while True:
            t = d.read(1)
            if not t:
                break
            data.append(t)
        data = jb2jb(data)
        data_list.append(data)
        print(data)
    sava('cqj', Info_Url, data_list, updateBy='cqj', remark=Title)


def spider2save(Title, Html, Info_Url, Imag_contnet, Imag_Urls, createBy, updateBy=None):
    data_list = list()
    data_list.append(Imag_contnet)
    for url_ in Imag_Urls:
        response = requests.get(url_)
        if response.status_code == 200:
            response.encoding = 'gbk'
        d = BytesIO(response.content)
        data = []
        while True:
            t = d.read(1)
            if not t:
                break
            data.append(t)
        data = jb2jb(data)
        data_list.append(data)
        # print(data)
    sava(createBy, Info_Url, data_list, updateBy=updateBy, remark=Title)


def sava(createBy, Info_Url, imageFile, updateBy=None, size=0, remark=None):
    dic = {
        "imageId": None,
        "createBy": createBy,
        "createTime": None,
        "updateBy": updateBy,
        "updateTime": None,
        "feature": 0,
        "size": size,
        "sourceURL": Info_Url,
        "hdfsPath": None,
        "fileExtname": "jpg",
        "remark": remark,
        "imageFile": imageFile
    }

    retry = 0
    while retry < 5:
        response = requests.post('http://120.26.166.175:8090/images/add', json=dic,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            logging.error('success')
            break
        else:
            retry += 1
            logging.error("status_code:{}, error_info:{}".format(response.status_code, response.text))


if __name__ == '__main__':
    imgPath = '2.jpg'
    savePath = '3.jpg'
    # 本地文件
    res = img2Bytes(imgPath)
    # print(res)
    # bytes2Img(res, savePath)
    # sava('cqj', 'https://www.baidu.com', res, 'cqj', remark='just test1')

    # 网络文件
    # url = 'https://p7.qhimg.com/bdm/1000_618_85/t0126965e612a7835ac.jpg'
    # response = requests.get(url)
    # if response.status_code == 200:
    #     response.encoding = 'gbk'
    # print(response.content)
    # d = BytesIO(response.content)
    # data = []
    # while True:
    #     t = d.read(1)
    #     if not t:
    #         break
    #     data.append(t)
    # d1 = jb2jb(data)  #
    # print(d1)
    # sava('cqj', url, d1, 'cqj', remark='halo哈喽')
    # bytes2Img(d1, savePath)
    # print('completed')

    # 传给大数据案例
    Info_Url = 'https://ss.netnr.com/wallpaper#26'
    Imag_Urls = ['https://p7.qhimg.com/bdm/1000_618_85/t0126965e612a7835ac.jpg',
                 'https://p9.qhimg.com/bdr/__100/t0153df2c1ccb1f5c1a.jpg']
    spider2save(Title='360壁纸', Html='html', Info_Url=Info_Url, Imag_contnet=res, Imag_Urls=Imag_Urls, createBy="Cc.")
