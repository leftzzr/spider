# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 16:47
# @Author  : 张梓锐
# @File    : 猎聘非异步.py
# @Software: PyCharm 
# @Content :

import requests
import aiohttp
import csv
import time
import ast
import random
import asyncio
import pandas as pd

from lxml import etree

num = 0  # 已爬取职位总数
there_headers = [
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'},
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
]
# Cookie = {'__gc_id': '3057bdb8b0da4c1082becff8dd9da5b5', ' Hm_lvt_a2647413544f5a04f00da7eee0d5e200': '1656225871',
#           ' __s_bid': '2645aa166cd2a85a95242cc330bcf2a62853', ' __uuid': '1656227524837.17',
#           ' __tlog': '1656227524867.69|00000000|00000000|00000000|00000000',
#           ' acw_tc': '2760829816562306829961971e231f86854809ab79abc0918079e76d9c5857', ' __session_seq': '8',
#           ' __uv_seq': '8', ' Hm_lpvt_a2647413544f5a04f00da7eee0d5e200': '1656230746'}
first_url_ = "https://www.liepin.com/zhaopin/?headId=75cf575e3cb974b23785624c4733d6fd&ckId=6cgvac0pjqr5apjlx7s5d2gh54hh22f8&oldCkId=be6c87f69c9dc46d084393f07254d8c3&fkId=drigwlru72prxf1nq2v0ma57i6r4uo3b&skId=njn4izjf8hl17j3bu51hm837dpeove3b&sfrom=search_job_pc&key=%E4%BA%BA%E5%8A%9B%E6%80%BB%E7%9B%91&compScale=080&currentPage=0&scene=page"
next_url_1 = "https://www.liepin.com/zhaopin/?headId=75cf575e3cb974b23785624c4733d6fd&ckId=6cgvac0pjqr5apjlx7s5d2gh54hh22f8&oldCkId=be6c87f69c9dc46d084393f07254d8c3&fkId=drigwlru72prxf1nq2v0ma57i6r4uo3b&skId=njn4izjf8hl17j3bu51hm837dpeove3b&sfrom=search_job_pc&key=%E4%BA%BA%E5%8A%9B%E6%80%BB%E7%9B%91&compScale=080&currentPage="
next_url_2 = "&scene=page"


# session = requests.session()
# session = aiohttp.ClientSession()
def get_header():
    # mm = random.randint(0, 2)  # 可设成随机header
    return there_headers[0]


# 可添加上https，但异步不支持https代理
all_proxy = [{'http': '27.44.43.132:4231'}, {'http': '121.8.28.135:4213'}, {'http': '183.7.121.144:4215'},
             {'http': '183.7.114.234:4215'}, {'http': '14.157.101.167:4213'}, {'http': '27.44.39.52:4231'},
             {'http': '113.65.232.86:4245'}, {'http': '183.7.131.212:4215'}, {'http': '183.7.14.205:4215'},
             {'http': '14.157.103.12:4213'}, {'http': '27.44.36.37:4231'}, {'http': '116.26.6.61:4215'},
             {'http': '27.44.37.125:4231'}, {'http': '14.157.104.82:4213'}, {'http': '14.157.100.252:4213'},
             {'http': '14.157.100.253:4213'}, {'http': '119.126.156.219:4213'}, {'http': '121.9.199.138:4213'},
             {'http': '116.22.51.229:4245'}, {'http': '119.126.156.211:4213'}]


proxy_num = 0  # 可理解为指向某个代理的指针


def get_proxy():
    global proxy_num  # 循环调用代理
    proxy_num += 1

    if proxy_num <= 20:
        return all_proxy[proxy_num - 1]
    else:
        proxy_num -= 20
        return all_proxy[proxy_num - 1]


def get_one_url(first_url):  # 获取一级页面url，并翻页
    session = requests.session()
    whether_next = get_two_url(session, one_url=first_url)  # 获取有无下一页
    pages = 10
    print("\n第{}页over\n".format(pages))
    while whether_next:
        print("翻页")
        next_url = next_url_1 + str(pages) + next_url_2
        whether_next = get_two_url(session, one_url=next_url)
        pages = pages + 1
        print("\n第{}页over\n".format(pages))


def get_two_url(session, one_url):  # 在一级2页面内获取二级页面的所有url
    response = session.get(one_url, headers=get_header(), proxies=get_proxy()).text
    # with open("aa.html", "w", encoding="utf-8") as c:  # 查看HTML格式
    #     c.write(response)
    #     c.write("........\n")
    tree = etree.HTML(response)
    all_two_url = []
    lists = tree.xpath('/html/body/div[1]/div/section[1]/div/ul/li')  # 二级url
    time.sleep(random.randint(0, 3))
    for li in lists:
        # tree_1 = etree.HTML(li)
        two_url = li.xpath('div/div/div[1]/div/a[1]/@href')[0]
        # print(two_url)
        all_two_url.append(two_url)
    traverse_two_url(session, all_two_url)  # 循环获取二级页面内容

    # 代理是短期代理，有效时长仅5-25分，如代理ip失效则会使用本机ip，多次爬虫后可能造成安全验证
    try:
        next_pages = tree.xpath('/html/body/div[1]/div/section[1]/div/div/ul/li[8]/@class')[0]
    except:
        print("翻页异常")  # 此处异常为next_pages的xpath路径发生了变化，举例倒数第三页之前都是li[8]/@class，倒数第二页则是变成了li[7]/@class，我没有修改
    if next_pages == "ant-pagination-next":  # 检查程序是否有下一页
        return True
    else:
        return False


def traverse_two_url(session, all_two_url): # 循环获取二级页面内容
    for url_2 in all_two_url:
        get_text(session, url_2)


def get_text(session, last_url):
    time.sleep(random.randint(0, 3))
    resp = session.get(last_url, headers=get_header(), proxies=get_proxy()).text
    with open("bb.html", "w", encoding="utf-8") as v:
        v.write(resp)  # 如果需要验证此处可看见bb.html显示为猎聘安全中心
        v.write(".............\n")
        global num
        num = num + 1
        print("num:", num)

    tree = etree.HTML(resp)
    try:
        text = tree.xpath('/html/body/main/content/section[2]/dl/dd/text()')[0]  # 正文（岗位需求职责等）
        name = tree.xpath('/html/body/section[3]/div[1]/div[1]/span[1]/text()')[0]  # 职位名称
        # money = tree.xpath('/html/body/section[3]/div[1]/div[1]/span[2]/text()')[0]  # 职位薪资
        # data = {"岗位名称": name, "岗位薪资": money, "岗位要求": text}
        # data = {"岗位名称": name, "岗位要求": text}
        # # dd = pd.read_csv("xx.csv", encoding="utf-8",error_bad_lines=False) #加入参数)
        # # print(dd)
        # i = pd.DataFrame(data, index=[num])
        # i.to_csv("xx.csv", index=True, mode='a', sep=",", encoding="UTF-8-sig")
        # print(name, "over")
        data = [num, name, text]  # 封装数据
        # print(data)
        with open('xx.csv', 'a', encoding='utf-8') as fps:
            writer = csv.writer(fps)
            writer.writerow(data)  # 将封装好的数据传入csv

    except:
        print("异常认证")  # 此处打一断点，可在程序中断时前往网页手动验证，也不打断点调用selenium自动完成验证


# resp = session.get(li, headers=headers).text
# # with open("yy.txt", "w", encoding="utf-8") as fp:
# #     fp.write(resp)
# t = etree.HTML(resp)
# text = t.xpath('/html/body/main/content/section[2]/dl/dd/text()')[0]
# with open("xx.txt", "a", encoding="utf-8") as f:
#     f.write(text)
#     f.write("...........................")
# print("over")

if __name__ == '__main__':
    get_one_url(first_url_)
    # print(type(get_header()))
    print("all over")
