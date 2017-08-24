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

import datetime

import imp
import tushare as ts

import time

from stock.models import Stock_Fenshi
from stockweb import settings


class DownloadFenShiThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que
        self.csv_retry_count = 0
        self.db_retry_count = 0
        self.tick_retry_count = 0

    def run(self):
        while True:
            if self.queue.empty():
                break
            code = self.queue.get()
            # processing the item
            # time.sleep(code)



            n = 0
            imp.acquire_lock()
            end = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
            imp.release_lock()

            while n < 730:
                n += 1
                print self.name,code, end
                socket.setdefaulttimeout(100)
                try:
                    df = ts.get_tick_data(code, end.date())
                    if type(df) != types.NoneType and df.index.size > 0 and 'alert' not in df.values[0][0]:
                        self.tick_retry_count = 0
                        self.download_fenshi_tocsv(code, end.date(), df)
                        # self.download_fenshi_todb(code, end.date(), df)
                    else:
                        print '       ----------no data'

                    end -= datetime.timedelta(days=1)
                except Exception as e:
                    print('get stock fenbi failed! code = [' + str(code) + '],date = [' + str(end.date()) + '] ,retruCount = [' + str(self.tick_retry_count) + '] , Error = [' + str(e) + ']')
                    self.get_tick_data(code,end)
                    end -= datetime.timedelta(days=1)

            print 'queue 大小:',self.queue.qsize()
            self.queue.task_done()
        return



    def get_tick_data(self,code,date):
        self.tick_retry_count += 1
        try:
            df = ts.get_tick_data(code, date.date())
            if type(df) != types.NoneType and df.index.size > 0 and 'alert' not in df.values[0][0]:

                self.download_fenshi_tocsv(code, date.date(), df)
                # self.download_fenshi_todb(code, end.date(), df)
            else:
                print '       ----------no data'
            print('get stock fenbi successed ! code = [' + str(code) + '],date = [' + str(date) + '] ,retruCount = [' + str(self.tick_retry_count) + ']')
            self.tick_retry_count = 0
        except Exception as e:
            print('get stock fenbi failed! code = [' + str(code) + '],date = ['+str(date)+'] ,retruCount = ['+str(self.tick_retry_count)+'] , Error = [' + str(e) + ']')
            self.get_tick_data(code,date)





    def download_fenshi_tocsv(self, code, date, df):
        path = settings.DOWNLOAD_PATH_FENSHI+str(code)+'/'
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            if os.path.exists(path + str(code) + '_' + str(date) + '.csv'):
                return

            df.to_csv(path + str(code) + '_' + str(date) + '.csv', encoding="utf_8_sig")
            print 'fenshi csv download successed , code = [ '+str(code)+' ] , retryCount = ['+str(self.csv_retry_count)+']'
            self.csv_retry_count = 0
        except Exception as e:
            self.csv_retry_count += 1
            print('download stock fenbi data to csv failed! code = [' + str(code) + '] ,date = [' + str(date) + '], retryCount = [' + str(self.csv_retry_count) + '], Error = [' + str(e) + '] ')
            self.download_fenshi_tocsv(code,date,df)


    def download_fenshi_todb(self, code, date, df):

        try:
            index = df.index.size
            for i in range(0, index):
                value = df.values[i]
                sf = Stock_Fenshi()
                sf.code = code
                sf.date = date
                sf.time = value[0]
                sf.price = value[1]
                if value[2] == '--':
                    sf.change = 0
                else:
                    sf.change = value[2]
                sf.volume = value[3]
                sf.amount = value[4]
                sf.type = value[5]
                sf.save()
            print 'fenshi insert to db successed ,code = ['+str(code)+']  total [' + str(index) + '] , retryCount = ['+str(self.db_retry_count)+']'
            self.csv_retry_count = 0
        except Exception as e:
            self.db_retry_count += 1
            print('download stock fenbi data to csv failed! code = [' + str(code) + '] , ,date = [' + str(date) + '], retryCount = [' + str(self.db_retry_count) + '],  Error = [' + str(e) + ']')
            self.download_fenshi_todb(code,date,df)