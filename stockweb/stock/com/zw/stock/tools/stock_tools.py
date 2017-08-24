#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/29 18:14
# @Author  : Aries
# @Site    : 
# @File    : stock_tools.py
# @Software: PyCharm

"""
股票工具类
"""
import types

import datetime

from stock.models import Current_Price_Of_Low_Rate


class StockTools(object):

    '''
        计算当前价格与最高价的比例
        @:param stock_data 股票信息，dict类型，key=股票代码，value=股票日K数据
    '''
    def getCurrentPriceOfHighRate(self, stock_data):
        currentPriceOfHighRate = {}
        if isinstance(stock_data, dict):
            for key in stock_data.keys():
                data = stock_data[key]
                #当前收盘价格
                cur_price = data[0][3]

                # 找出最高价
                high = float(data[0][2])
                for i in range(1,len(data)):
                    if float(data[i][2])>high:
                        high = float(data[i][2])
                currentPriceOfHighRate[key] = float(cur_price)/high
        else:
            print 'stock_data type error'

        return currentPriceOfHighRate



    '''
        计算当前价格与最低价的比例
        @:param stock_data 股票信息，dict类型，key=股票代码，value=股票日K数据
        currentPriceOfLowRateTrue：放量且均线多头排列
        currentPriceOfLowRateFalse：不满足放量且均线多头排列
    '''
    def getCurrentPriceOfLowRate(self, stock_data):
        currentPriceOfLowRateTrue = {}
        currentPriceOfLowRateFalse = {}
        if isinstance(stock_data, dict):

            # 放量、大涨标志
            for key in stock_data.keys():
                data = stock_data[key]
                #当前日期
                current_date = data[0][0]
                # 当前收盘价格
                cur_price = data[0][3]
                # 最高价格出现的日期
                highDate = data[0][0]
                #换手率
                turnover = data[0][14]

                # 找出最高价
                high = float(data[0][2])
                # 最高价在数据中的位置
                index = 0
                for i in range(1, len(data)):
                    if float(data[i][2]) > high:
                        high = float(data[i][2])
                        highDate = data[i][0]
                        index = i

                # 判断当前是否处于最低价，如果是则统计，否则跳过
                min = float(data[0][3])  # 最近（当天收盘价）
                minDate = data[0][0]
                for i in range(1, index):
                    if float(data[i][4]) < min:
                        min = float(data[i][4])  # 找出最低价
                        minDate = data[i][0]
                # print str(key)+' 在 ' + str(minDate) + ' 出现最低价 '+ str(min)

                # 判断涨幅是否大于5% 和量能是否放量
                rate = 0;
                cpolr = None
                rate = float(cur_price) / min
                if float(data[0][7]) > 5 and float(data[0][5]) > float(data[0][11]) and float(data[0][5]) > float(
                        data[0][12]) and float(data[0][5]) > float(data[0][13]) and float(data[0][14]) > 5 \
                        and float(data[0][8]) > float(data[0][9]) > float(data[0][10]):

                    currentPriceOfLowRateTrue[key] = rate
                    cpolr = Current_Price_Of_Low_Rate(code=key,current_price=cur_price,current_date=current_date,
                                              high_price =high,high_date=highDate,low_price=min,low_date=minDate,rate=rate,ave_price_up=1,volume_up=1,turnover=turnover )
                else:
                    currentPriceOfLowRateFalse[key] = rate
                    cpolr = Current_Price_Of_Low_Rate(code=key, current_price=cur_price, current_date=current_date,
                                                      high_price=high, high_date=highDate, low_price=min,
                                                      low_date=minDate, rate=rate, ave_price_up=0, volume_up=0,turnover=turnover)
                #判重
                exist = Current_Price_Of_Low_Rate.objects.filter(code=key,current_date=current_date)
                if len(exist)<=0:
                    #数据不存在，创建
                    cpolr.save()

        else:
            print 'stock_data type error'
        print currentPriceOfLowRateTrue, currentPriceOfLowRateFalse
        return (currentPriceOfLowRateTrue, currentPriceOfLowRateFalse)

