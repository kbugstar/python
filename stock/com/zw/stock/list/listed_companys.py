#coding=utf-8

'''
A股所有股票集合
'''
import socket

import tushare as ts
import sys

from stock.com.zw.db import db_operator
from stock.com.zw.utils import logger_factory

reload(sys)
sys.setdefaultencoding('utf-8')

'''数据库连接池'''
dbOperator =db_operator.DBoperator()
'''表名'''
table = "wealth_stocks"

class DownStockBasic(object):
    def __init__(self):
        self.__logger = logger_factory.getLogger("downloadStockList")

    '''
        下载股票信息到csv文件
    '''
    def download_stock_basic_info_tocsv(self):
        try:
            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()
            #直接保存到csv
            print 'choose csv'
            stock_list.to_csv('../file/csv/listed_stock_basic_list.csv')
            print('download csv finish')

        except Exception as e:
            self.__logger.error('download stock list basic to csv failed >>> ' + str(e))
            pass


    '''
        下载股票信息并入库
    '''
    def download_stock_basic_info_todb(self):
        try:
            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()

            # 入库
            index = stock_list.index.size
            print('code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket')
            stock = {}
            stock_dict = []
            for i in range(0, index):
                # 获取股票代码
                stock['code'] = stock_list.index.values[i]
                # 获取股票信息
                value = stock_list.values[i]
                # 获取股票具体信息
                stock['name'] = str(value[0]).decode(encoding='utf-8', errors='name解码错误,code=[' + stock['code'] + ']')
                stock['industry'] = str(value[1]).decode(encoding='utf-8', errors='industry解码错误,code=[' + stock['code'] + ']')
                stock['area'] = str(value[2]).decode(encoding='utf-8', errors='area解码错误,code=[' + stock['code'] + ']')
                stock['pe'] = str(value[3])
                stock['outstanding'] = str(value[4])
                stock['totals'] = str(value[5])
                stock['totalAssets'] = str(value[6])
                stock['liquidAssets'] = str(value[7])
                stock['fixedAssets'] = str(value[8])
                stock['reserved'] = str(value[9])
                stock['reservedPerShare'] = str(value[10])
                stock['esp'] = str(value[11])
                stock['bvps'] = str(value[12])
                stock['pb'] = str(value[13])
                stock['timeToMarket'] = str(value[14])

                # print(stock)
                if not self.isExistStock(stock['code']):
                    dbOperator.insertIntoDB(table, stock)
                # stock_dict.append(stock)



        except Exception as e:
            self.__logger.error('download stock list basic to db failed >>> ' + str(e))
            pass


    '''
        根据股票代码（code）判断库中是否存在该股票
    '''
    def isExistStock(self,code):
        sql = 'SELECT * FROM ' + table + ' where code = ' + code
        n = dbOperator.execute(sql)
        if n > 0:
            return True
        return False





if __name__ == '__main__':
    DownStockBasic().download_stock_basic_info_tocsv()
    # DownStockBasic().download_stock_basic_info_todb()

