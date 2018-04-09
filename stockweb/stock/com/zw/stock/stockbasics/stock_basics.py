#coding=utf-8

'''
A股所有股票集合
'''
import os
import socket
import types

import tushare as ts
import sys

from stock.com.zw.db import db_operator
from stock.com.zw.utils import logger_factory
from stockweb.stock.com.zw.utils.date_utils import DateUtils
from stockweb.stock.models import Stock_Basics
from stockweb.stockweb import settings

reload(sys)
sys.setdefaultencoding('utf-8')

'''数据库连接池'''
dbOperator =db_operator.DBoperator()
'''表名'''
table = "wealth_stocks"

class DownLoadStockBasic(object):
    def __init__(self):
        self.__logger = logger_factory.getLogger("downloadStockList")

    '''
        下载股票信息到csv文件
    '''
    def download_stock_basic_info_tocsv(self,path):


        try:
            if not os.path.exists(path):
                os.makedirs(path)
            # self.__logger.info('begining download stock history data to csv! code = [' + str(code) + ']')
            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()
            if type(stock_list) != types.NoneType:
                stock_list.to_csv(path + str(DateUtils().get_current_date())+'.csv', encoding="utf_8_sig")
        except Exception as e:
            print(
                'download stock basics data failed!  Error = [' + str(e) + ']')



    '''
        下载股票信息并入库
    '''
    def download_stock_basic_info_todb(self):
        try:
            path = settings.DOWNLOAD_PATH_STOCKBASICS
            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()

            # 入库
            index = stock_list.index.size
            print('code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket')
            stock = {}
            stock_dict = []
            for i in range(0, index):
                sb = Stock_Basics()
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

                stock['undp'] = str(value[15])
                stock['perundp'] = str(value[16])
                stock['rev'] = str(value[17])
                stock['profit'] = str(value[18])
                stock['gpr'] = str(value[19])
                stock['npr'] = str(value[20])
                stock['holders'] = str(value[21])

                # 获取股票代码
                sb.code = stock_list.index.values[i]
                # 获取股票信息
                value = stock_list.values[i]
                # 获取股票具体信息
                sb.name = str(value[0]).decode(encoding='utf-8', errors='name解码错误,code=[' + sb.code + ']')
                sb.industry = str(value[1]).decode(encoding='utf-8', errors='industry解码错误,code=[' + sb.code + ']')
                sb.area = str(value[2]).decode(encoding='utf-8', errors='area解码错误,code=[' + sb.code + ']')
                sb.pe = str(value[3])
                sb.outstanding = str(value[4])
                sb.totals = str(value[5])
                sb.totalAssets = str(value[6])
                sb.liquidAssets = str(value[7])
                sb.fixedAssets = str(value[8])
                sb.reserved = str(value[9])
                sb.reservedPerShare = str(value[10])
                sb.esp = str(value[11])
                sb.bvps = str(value[12])
                sb.pb = str(value[13])
                sb.timeToMarket = str(value[14])

                sb.undp = str(value[15])
                sb.perundp = str(value[16])
                sb.rev = str(value[17])
                sb.profit = str(value[18])
                sb.gpr = str(value[19])
                sb.npr = str(value[20])
                sb.holders = str(value[21])

                print(stock)
                sb.save()
                if not self.isExistStock(stock['code']):
                    dbOperator.insertIntoDB(table, stock)
                stock_dict.append(stock)



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
    path = settings.DOWNLOAD_PATH_STOCKBASICS
    #path = 'E:/stock/csv/stockbasics/'

    # DownStockBasic().download_stock_basic_info_tocsv(path)
    DownStockBasic().download_stock_basic_info_todb()
    # DownStockBasic().download_stock_basic_info_todb()

