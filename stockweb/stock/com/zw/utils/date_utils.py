#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/26 0026 18:36
# @Author  : Aries
# @Site    : 
# @File    : date_utils.py
# @Software: PyCharm
import datetime


class DateUtils():

    def __init__(self):
        #格式化输出
        self.DATEFORMAT = '%Y%m%d'  # 设置输出格式

    '''
        获取当天日期，格式：20161226
    '''
    def get_current_date(self):
        today = datetime.date.today()
        return today.strftime(self.DATEFORMAT)

    '''
        将 20170122 日期格式转换成 2017-01-22
    '''
    def turn_date(self,date):
        if len(date) != 8:
            return None

        date = date[0:4]+'-'+date[4:6]+'-'+date[6:]
        return date








if __name__=='__main__':
    # DateUtils().get_current_date()
    print  DateUtils().turn_date('20170122')