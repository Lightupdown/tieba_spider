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
import os
import socket


def IsOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        print('%d is open' % port)
        return True
    except:
        print('%d is down' % port)
        return False
if __name__ == '__main__':
    str_name = ['天涯明月刀ol吧']
    str_list = ('[', ']')
    str_name.remove(str_list)
    print(str_name)

