#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/27 14:58
# @Author  : Aries
# @Site    : 
# @File    : mongo_utils.py
# @Software: PyCharm
from pymongo import MongoClient


class MongoUtils():

    def __init__(self):
        # 建立连接
        self.mongoClient = MongoClient()
        '''
        上句等同于：
            client = MongoClient(“localhost”, 27017)
            client = MongoClient(“mongodb://localhost:27017/”)
        '''