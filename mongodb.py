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
import datetime
from pymongo import MongoClient

# 连接数据库
client = MongoClient()
# client = MongoClient('127.0.0.1', 27017)
# client = MongoClient('mongodb://localhost:27017/')

# 获取数据库
db = client.python_db_test
# db = client['python-db']

# 获取集合
collection = db.python_collection
# collection = db['python-collection']

post = {
    'author': 'zhang',
    'text': 'My first bolg post!',
    'tags': ['mongodb', 'python', 'pymongo'],
    'date': datetime.datetime.utcnow()
}

posts = db.posts
posts_id = posts.insert_one(post).inserted_id
print('post id is : ', posts_id)
