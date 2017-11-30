#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = ''
__author__ = 'zhang'
__mtime__  = '2017/11/29'

              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import re

from lxml import etree
from random import choice
from pymongo import MongoClient

import requests
import time

headers = {'User-Agent': '',
           'cookie': 'BAIDUID=9EE26C9FDE87C48D0B0FBBB8EBF5A6D6:FG=1; BIDUPSID=7353161D76B91C28B7E137EE68051B15; '
                     'PSTM=1510217298; TIEBA_USERTYPE=eaa5821f8b6e4050e8f74ee3; BDRCVFR[DyfsikfAVJf]=mk3SLVN4HKm; '
                     'fixed_bar=1; FP_UID=7a3af4a3371d9022b131198e2b719494; BDUSS=045aUlHUXVoMVZiSWM4QlZwTVFXNmdVY'
                     'VRKM1JRd0MxVFVUaXY0dlAwYS1xRVZhQUFBQUFBJCQAAAAAAAAAAAEAAADvfWw5wLbvpLfj0u0AAAAAAAAAAAAAAAAAAA'
                     'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL4bHlq-Gx5aU; STOKEN=d5c96a9ceaedf6f8b8'
                     'fb05e4b699aeeb275527751f73698c57d3cfe1e841016c; TIEBAUID=a42b78ec9b44da1d8e02f249; BDRCVFR[TBT'
                     '3PkAMHw_]=mk3SLVN4HKm; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_WISE_SIDS=120066_'
                     '102572_114552_102524_104599_119482_100099_120162_110773_118879_118867_118843_118821_118788_1073'
                     '17_119044_118969_120667_117580_117327_117240_120634_117432_120595_118965_118103_117555_116146_'
                     '119963_119929_118296_120263_116408_110085_120807; PSINO=2; IS_NEW_USER=eaa5821f89c24250e9f74e8'
                     'f; BAIDU_WISE_UID=wapp_1511923673085_405; CLIENTWIDTH=414; CLIENTHEIGHT=736; mo_originid=1; '
                     'bdps_login_cookie=19; SEENKW=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C; LASW=414; USER_JUMP=1; '
                     'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1511830488,1511922338,1511923632,1511923668; '
                     'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1511924235'}
# proxies = {"http": ''}
cookies = {'cookie': 'BAIDUID=9EE26C9FDE87C48D0B0FBBB8EBF5A6D6:FG=1; BIDUPSID=7353161D76B91C28B7E137EE68051B15; '
                     'PSTM=1510217298; TIEBA_USERTYPE=eaa5821f8b6e4050e8f74ee3; BDRCVFR[DyfsikfAVJf]=mk3SLVN4HKm; '
                     'fixed_bar=1; FP_UID=7a3af4a3371d9022b131198e2b719494; BDUSS=045aUlHUXVoMVZiSWM4QlZwTVFXNmdVY'
                     'VRKM1JRd0MxVFVUaXY0dlAwYS1xRVZhQUFBQUFBJCQAAAAAAAAAAAEAAADvfWw5wLbvpLfj0u0AAAAAAAAAAAAAAAAAAA'
                     'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL4bHlq-Gx5aU; STOKEN=d5c96a9ceaedf6f8b8'
                     'fb05e4b699aeeb275527751f73698c57d3cfe1e841016c; TIEBAUID=a42b78ec9b44da1d8e02f249; BDRCVFR[TBT'
                     '3PkAMHw_]=mk3SLVN4HKm; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_WISE_SIDS=120066_'
                     '102572_114552_102524_104599_119482_100099_120162_110773_118879_118867_118843_118821_118788_1073'
                     '17_119044_118969_120667_117580_117327_117240_120634_117432_120595_118965_118103_117555_116146_'
                     '119963_119929_118296_120263_116408_110085_120807; PSINO=2; IS_NEW_USER=eaa5821f89c24250e9f74e8'
                     'f; BAIDU_WISE_UID=wapp_1511923673085_405; CLIENTWIDTH=414; CLIENTHEIGHT=736; mo_originid=1; '
                     'bdps_login_cookie=19; SEENKW=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C; LASW=414; USER_JUMP=1; '
                     'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1511830488,1511922338,1511923632,1511923668; '
                     'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1511924235'}

tieba_info = {'a': '',
              'img': '',
              'ba_name': '',
              'ba_m_num': '',
              'ba_p_num': '',
              'ba_desc': ''
              }
tieba_infos = []

def fetch():
    flag = 0
    proxy_host = ''
    html_content = 1
    re_tieba = re.compile(r'^\[\'(.*)\'\]$')

    client = MongoClient()
    db = client.tieba
    posts = db.posts

    # 手机版
    # url = r'https://tieba.baidu.com/mo/q/catalog'
    # data = {
    #     'tn': 'detail',
    #     'pmname': '游戏玩家',
    #     'pmid': 179,
    #     'pmtype': 0,
    #     'mid': 179,
    #     'mtype': 0,
    #     'mname': '游戏玩家',
    #     'st_type': 'catalog_level2'
    # }
    # 电脑版
    url = 'http://tieba.baidu.com/f/index/forumpark'
    data = {
        'cn': r'客户端网游',
        'ci': '0',
        'pcn': r'游戏',
        'pci': '0',
        'ct': '1',
        'st': r'new',
        'pn': 1
    }
    # url = r'http://tieba.baidu.com/f/index/forumpark?cn=客户端网游&ci=0&pcn=游戏&pci=0&ct=1&st=new&pn=1'

    while html_content:
        tieba_infos = []

        # # 每10次换一次User-Agent：
        # if flag % 10 == 0 or flag == 0:
        #     flag = 0
        #     headers['User-Agent'] = get_random_user_agent()

        # 每5次换一次ip代理：
        if flag % 5 == 0 or flag == 0:
            proxy_host = get_random_agency_ip()
        time.sleep(1)
        try:
            # proxies={"http": proxy_host},
            html = requests.get(url, params=data, timeout=10)
        except Exception as e:
            print(e)
            continue
        finally:
            flag += 1
        html_content = html.content.decode('utf-8')
        print('url: ', html.url)
        print('html_content: ', html_content)
        seletor = etree.HTML(html_content)
        ba_info = seletor.xpath("//div[@class='right-sec']/div[@class='ba_list clearfix']/div[@class='ba_info']")
        print('action~~~~~~~~~~')
        for ba_info_info in ba_info:
            # 贴吧链接，只有后面一段
            a = str(ba_info_info.xpath("a[1]/@href"))
            str_a = re_tieba.match(a).group(1)
            tieba_info['a'] = str_a
            print('a: ', str_a)
            # 贴吧头像
            img = ba_info_info.xpath("a/img/@src")
            str_img = re_tieba.match(img).group(1)
            tieba_info['img'] = str_img
            print('img: ', str_img)
            # 贴吧名
            ba_name = ba_info_info.xpath("a/div[1]/p[1]/text()")
            str_ba_name = re_tieba.match(ba_name).group(1)
            tieba_info['ba_name'] = str_ba_name
            print('ba_name: ', str_ba_name)
            # 关注人数
            ba_m_num = ba_info_info.xpath("a/div[1]/p[2]/span[1]/text()")
            str_ba_m_num = re_tieba.match(ba_m_num).group(1)
            tieba_info['ba_m_num'] = str_ba_m_num
            print('ba_m_num: ', str_ba_m_num)
            # 发帖数
            ba_p_num = ba_info_info.xpath("a/div[1]/p[2]/span[2]/text()")
            str_ba_p_num = re_tieba.match(ba_p_num).group(1)
            tieba_info['ba_p_num'] = str_ba_p_num
            print('ba_desc: ', str_ba_p_num)
            # 简介
            ba_desc = ba_info_info.xpath("a/div[1]/p[3]/text()")
            str_ba_desc = re_tieba.match(ba_desc).group(1)
            tieba_info['ba_desc'] = str_ba_desc
            print('ba_desc: ', str_ba_desc)
            # 往列表里添加字典，一会一块存进去
            tieba_infos.append(tieba_info)
        # 翻页
        data['pn'] += 1
        # mongodb数据库存储tieba_infos
        posts.insert(tieba_infos)

def get_random_agency_ip():
    '''
    从get_agency_ip.TYPE+'proxynew.txt'（姑且称其IP池）中随机取一个IP地址返回
    :return:   IP+port   string类型
    '''
    # 请注意此处的 ip池'proxynew.txt'，将其改成你的文件名
    with open('ntproxynew.txt', 'r') as f:
        ip_lines = f.readlines()
    for i in range(len(ip_lines)):
        ip_lines[i] = ip_lines[i].replace('\n', '')
        # print('line: ', ipLines[i])
    random_ip = 'http://' + choice(ip_lines)
    print('从IP池中取得代理IP： ', random_ip)
    return random_ip


def get_random_user_agent():
    '''
    从user-agent-android.txt（UA池）中随机取得一个UA返回
    :return: user-agent   string类型
    '''
    with open('user_agent_windows.txt', 'r') as f:
        agent_lines = f.readlines()
    for i in range(len(agent_lines)):
        agent_lines[i] = agent_lines[i].replace('\n', '')
    random_agent = choice(agent_lines)
    print('从UA池中取得user-agent: ', random_agent)
    return random_agent

if __name__ == '__main__':
    fetch()
