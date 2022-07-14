# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 15:41
# @Author  : 张梓锐
# @File    : 猎聘.py
# @Software: PyCharm 
# @Content :
import aiofiles
import requests
import aiohttp
import time
import ast
import random
import asyncio
import pandas as pd

from lxml import etree
num = 0
there_headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'},
     # {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'}
]
Cookie = {'__gc_id': '3057bdb8b0da4c1082becff8dd9da5b5', ' Hm_lvt_a2647413544f5a04f00da7eee0d5e200': '1656225871', ' __s_bid': '2645aa166cd2a85a95242cc330bcf2a62853', ' __uuid': '1656227524837.17', ' __tlog': '1656227524867.69|00000000|00000000|00000000|00000000', ' acw_tc': '2760829816562306829961971e231f86854809ab79abc0918079e76d9c5857', ' __session_seq': '8', ' __uv_seq': '8', ' Hm_lpvt_a2647413544f5a04f00da7eee0d5e200': '1656230746'}
first_url_ = "https://www.liepin.com/zhaopin/?headId=1b371c4343f0b7c1e3406d3c3bb1c6d1&ckId=s2vb0x96lxivk8mzo2wihg7uxf52t0a8&fkId=eb1ed03d0fb7122c4706ab1561d88c2c&skId=eb1ed03d0fb7122c4706ab1561d88c2c&sfrom=search_job_pc&key=%E4%BA%BA%E5%8A%9B%E8%B5%84%E6%BA%90&compScale=080&scene=condition"
next_url_1 = "https://www.liepin.com/zhaopin/?headId=ca69e0ff2e8f1640745f1e82789f55ce&ckId=u2hod9f6y2r5huowfh3tlk7zebfep618&oldCkId=ca69e0ff2e8f1640745f1e82789f55ce&sfrom=search_job_pc&key=%E4%BA%BA%E5%8A%9B%E8%B5%84%E6%BA%90&currentPage="
next_url_2 = "&scene=page"
# session = requests.session()
# session = aiohttp.ClientSession()
def get_header():
    mm = random.randint(0, 2)
    return there_headers[mm]

def get_proxy():
    with open("ff.txt", "r", encoding="utf-8") as fp:
        li = ast.literal_eval(fp.read())
        # return li[str(random.randint(0, 40))]
        return "http://120.37.95.154:4224"

async def get_one_url(first_url):
    async with aiohttp.ClientSession() as session:
        whether_next = await get_two_url(session, one_url=first_url)
        pages = 1
        while whether_next:
            next_url = next_url_1 + str(pages) + next_url_2
            whether_next = await get_two_url(session, one_url=next_url)
            pages = pages + 1


async def get_two_url(session, one_url):
    async with session.get(one_url, headers=get_header(), proxy=get_proxy()) as r:
        print(1)
        response = await r.text()
    # with open("zz.txt", "w", encoding="utf-8") as fp:
    #     fp.write(response)
    with open("aa.html", "a", encoding="utf-8") as c:
        c.write(response)
        c.write(".........................................................................................\n")
    tree = etree.HTML(response)
    all_two_url = []
    lists = tree.xpath('/html/body/div[1]/div/section[1]/div/ul/li')  # [2]/div/div/div[1]/div/a[1]/@href
    time.sleep(random.randint(0, 3))
    for li in lists:
        # tree_1 = etree.HTML(li)
        two_url = li.xpath('div/div/div[1]/div/a[1]/@href')[0]
        # print(two_url)
        all_two_url.append(two_url)
    await traverse_two_url(session, all_two_url)
    next_pages = tree.xpath('/html/body/div[1]/div/section[1]/div/div/ul/li[8]/@class')[0]
    if next_pages == "ant-pagination-next":
        return True
    else:
        return False


async def traverse_two_url(session, all_two_url):
    tasks = []
    for url_2 in all_two_url:
        tasks.append(get_text(session, url_2))
    await asyncio.wait(tasks)


async def get_text(session, last_url):
    time.sleep(random.randint(0, 3))
    async with session.get(last_url, headers=get_header(), proxy=get_proxy()) as r:
        resp = await r.text()
    with open("bb.html", "a", encoding="utf-8") as v:
        v.write(resp)
        v.write(".............")
        global num
        num = num + 1
        print("num:", num)
    print(2)
    tree = etree.HTML(resp)
    text = tree.xpath('/html/body/main/content/section[2]/dl/dd/text()')[0]
    name = tree.xpath('/html/body/section[3]/div[1]/div[1]/span[1]/text()')[0]
    money = tree.xpath('/html/body/section[3]/div[1]/div[1]/span[3]/text()')[0]
    data = {"岗位名称": name, "岗位薪资": money, "岗位要求": text}
    # dd = pd.read_csv("xx.csv", encoding="utf-8",error_bad_lines=False) #加入参数)
    # print(dd)
    i = pd.DataFrame(data, index=[num])
    i.to_csv("xx.csv", index=True,mode='a', sep=",", encoding="UTF-8-sig")
    print(3)


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
    asyncio.run(get_one_url(first_url_))
    # print(type(get_header()))
    print("over")