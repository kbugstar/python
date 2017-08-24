#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/30 0030 11:03
# @Author  : Aries
# @Site    : 
# @File    : testdb.py
# @Software: PyCharm
import os

from django.conf import settings

from stockweb.stock.models import Current_Price_Of_Low_Rate


def insert():
    os.environ.update({"DJANGO_SETTINGS_MODULE": "config.settings"})
    cpolr = Current_Price_Of_Low_Rate(code=000001,current_price=1,current_date='2016-12-30',high_price=2,high_date='2016-11-11',low_price=0.4,low_date='2016-02-22',rate=1.2,ave_price_up=1,volume_up=1)
    cpolr.save()