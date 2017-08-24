#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/19 0019 17:34
# @Author  : Aries
# @Site    : 
# @File    : his_fenbi.py
# @Software: PyCharm
import os
import socket
import types

import  tushare as ts

from stockweb.stockweb import settings

'''
    获取历史分笔数据
'''


class Fenbi():

    def get_his_fenbi_data(self,code,date):
        path = settings.DOWNLOAD_PATH_FENSHI
        #path = 'E:/stock/csv/fenbi/'
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            # self.__logger.info('begining download stock history data to csv! code = [' + str(code) + ']')
            socket.setdefaulttimeout(100)
            df = ts.get_tick_data(code,date)
            if type(df) != types.NoneType:
                df.to_csv(path + str(code) + '.csv',encoding="utf_8_sig")
                # self.__logger.info('download stock history data to csv successful! code = [' + str(code) + ']')
        except Exception as e:
            print(
                'download stock fenbi data failed! code = [' + str(code) + '] , Error = [' + str(e) + ']')




if __name__=='__main__':
    Fenbi().get_his_fenbi_data('600848','2014-01-09')