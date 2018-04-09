#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/28 21:25
# @Author  : Aries
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import socket
from time import ctime
import time

import datetime
import tushare as ts

from stock.com.zw.db.connection_pool import DbConnection
from stock.com.zw.stock.kline.stock_kline import StockKLine
from stock.com.zw.stock.tools.stock_tools import StockTools
from stock.com.zw.utils.file_utils import FileUtils
from stockweb.stock.com.zw.utils.date_utils import DateUtils

if __name__ == '__main__':

    path = '/tmp/stock/csv/fenshi/' +str(DateUtils().get_current_date())+'/'
    # data = ts.get_h_data(code='000852')
    # data.to_csv("hdata.csv")
    #
    #
    #
    # path = 'E:/stock/csv/learn/'
    # print '=====================start ....'+str(ctime())+'======================='
    #
    # print 'start download stock history data...'+str(ctime())
    # sk = StockKLine(DbConnection().create_connection_pool().connection())
    # code = None
    # failCodes = []
    # try:
    #     socket.setdefaulttimeout(100)
    #     stock_list = ts.get_stock_basics()
    #
    #     # 入库
    #     index = stock_list.index.size
    #
    #     for i in range(0, index):
    #         # 获取股票代码
    #         code = stock_list.index.values[i]
    #         sk.get_his_data_tocsv(code,path)
    # except Exception as e:
    #     if code != None:
    #         failCodes.append(code)
    #     print('download 【' + code + '】 stock his data  failed >>> ' + str(e))
    #     pass
    #
    # while len(failCodes) > 0:
    #     sk.get_his_data_tocsv(failCodes.pop(),path)
    #
    # print 'end download stock history data...' + str(ctime()) + '  tatal ['+str(index)+']'

    print 'start computing....' + str(ctime())
    fu = FileUtils()
    headers = None
    content = {}
    headers = {}
    files = fu.listDir(path)
    for file in files:
        code = file.split("/")[6][:6]
        header,data =fu.loadCsv(file)
        content[code] = data
        headers[code] = header

    # currentPriceOfHighRate = StockTools().getCurrentPriceOfHighRate(content)
    currentPriceOfLowRate = StockTools().getCurrentPriceOfLowRate(content, headers)
    #对计算结果的比例进行排序，从小到大
    #sorted方法：参数1：获取dict的key、value，用于排序
    #           参数2：key指定用于排序的列：d:d[0]：表示用第一个元素排序，即key  d:d[1]：表示用第二个元素排序，即value
    #           参数3：reverse：是否进行反转，默认为False，默认排序从小到大，reverse=True表示从大到小排序
    # currentPriceOfHighRate = sorted(currentPriceOfHighRate.iteritems(),key=lambda d:d[1],reverse=False)
    currentPriceOfLowRate = sorted(currentPriceOfLowRate.iteritems(),key=lambda d:d[1],reverse=False)

    # print currentPriceOfHighRate
    print currentPriceOfLowRate
    print 'end computing....'+str(ctime())
    print '=====================end  .... '+str(ctime())+'======================='