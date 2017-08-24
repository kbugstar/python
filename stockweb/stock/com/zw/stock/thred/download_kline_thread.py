#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/13 0013 10:27
# @Author  : Aries
# @Site    : 
# @File    : download_kline_thread.py
# @Software: PyCharm
import os
import socket
import threading
import types
import tushare as ts

import time

from stockweb import settings


class DownloadKlineThread(threading.Thread):
    def __init__(self, que,path):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que
        self.path = path

    def run(self):
        while True:
            if self.queue.empty():
                break
            code = self.queue.get()
            # processing the item
            # time.sleep(code)
            print self.name, code
            self.download_code(code,self.path)
            self.queue.task_done()
        return

    def download_code(self,code,path):
        # print 'download_code'
        path = settings.DOWNLOAD_PATH_KLINE
        #path = 'E:/stock/csv/kline/'  # +str(DateUtils().get_current_date())+'/'

        failCodes = []
        try:
            socket.setdefaulttimeout(100)
            self.downloadDataToCsv(code, path)
            print '【' + str(code) + '】 数据下载成功！'
        except Exception as e:
            if code != None:
                failCodes.append(code)
            print '【' + str(code) + '】  数据下载失败！ 原因： ' + str(e)
            pass
        cnt = 1
        while len(failCodes) > 0:
            print '第' + str(cnt) + '次循环，' + str(len(failCodes)) + '条失败'
            self.downloadDataToCsv(failCodes.pop(), path)


    def downloadDataToCsv(self,code, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            socket.setdefaulttimeout(100)
            # self.__logger.info('begining download stock history data to csv! code = [' + str(code) + ']')
            stock_data = ts.get_hist_data(code)
            if type(stock_data) != types.NoneType:
                stock_data.to_csv(path + str(code) +  '.csv')
                # self.__logger.info('download stock history data to csv successful! code = [' + str(code) + ']')
        except Exception as e:
            print(
                'download stock history data failed! code = [' + str(code) + '] , Error = [' + str(e) + ']')
