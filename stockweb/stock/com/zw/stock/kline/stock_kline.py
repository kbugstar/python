#coding:utf-8
import os
import socket
import types

import tushare as ts

from stock.com.zw.db import db_operator
from stock.com.zw.db.connection_pool import DbConnection
from stock.com.zw.utils import logger_factory


'''
    获取股票历史交易数据
    使用接口：get_h_data
    参数：
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取当前日期
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取去年今日
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
      drop_factor : bool, 默认 True
                是否移除复权因子，在分析过程中可能复权因子意义不大，但是如需要先储存到数据库之后再分析的话，有该项目会更加灵活
'''




class StockKLine(object):

    def __init__(self):
        self.__logger = logger_factory.getLogger('StockKLine')
        '''数据库连接池'''
        # self.dbOperator = db_operator.DBoperator(dbconnection)
        '''表名'''
        self.table = "stock_his_data"



    '''
        获取股票历史交易数据到csv文件
    '''
    def get_his_data_tocsv(self,code,path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            socket.setdefaulttimeout(100)
            # self.__logger.info('begining download stock history data to csv! code = [' + str(code) + ']')
            stock_data = ts.get_hist_data(code)
            if type(stock_data) != types.NoneType:
                stock_data.to_csv(path + 'stock_his_data_' + str(code) + '.csv')
            # self.__logger.info('download stock history data to csv successful! code = [' + str(code) + ']')
        except Exception as e:
            self.__logger.error('download stock history data failed! code = [' + str(code) + '] , Error = [' + str(e) +']' )

    '''
        获取股票历史交易数据并入库
    '''
    def get_his_data_todb(self,code):
        try:
            # print type(code)
            # #判断数据类型，通过多线程传过来list参数集合，取出其中的code
            if type(code) is types.ListType:
                code = code[0]
            socket.setdefaulttimeout(100)
            stock_his_data = ts.get_hist_data(code)

            # 入库
            index = stock_his_data.index.size
            #判断当前股票代码数据条数与库中数据条数是否相同，如果相同，直接跳过
            db_count = self.getCodeCount(code)
            if index == db_count:
                print '[' + str(code) + '] 历史数据已存在，共【' + str(db_count) + '】条'
            else:
                # print(
                # '日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率')
                his_data = {}
                for i in range(0, index):
                    # 获取股票代码
                    his_data['code'] = code
                    # 获取日期
                    his_data['date'] = stock_his_data.index.values[i]
                    # 获取股票信息
                    value = stock_his_data.values[i]
                    # 获取股票具体信息
                    his_data['open'] = str(value[0])
                    his_data['high'] = str(value[1])
                    his_data['close'] = str(value[2])
                    his_data['low'] = str(value[3])
                    his_data['volume'] = str(value[4])
                    his_data['price_change'] = str(value[5])
                    his_data['p_change'] = str(value[6])
                    his_data['ma5'] = str(value[7])
                    his_data['ma10'] = str(value[8])
                    his_data['ma20'] = str(value[9])
                    his_data['v_ma5'] = str(value[10])
                    his_data['v_ma10'] = str(value[11])
                    his_data['v_ma20'] = str(value[12])
                    his_data['turnover'] = str(value[13])

                    # print his_data['code'],his_data['date']
                    # if not self.isExistStock(his_data['code'],his_data['date']):
                    #     self.dbOperator.insertIntoDB(self.table, his_data)
                        # stock_dict.append(stock)

                print '['+str(code)+'] 历史数据新入库，共【'+ str(index) +'】条'

        except Exception as e:
            self.__logger.error('download stock list basic to db failed with code ['+str(code)+']>>> ' + str(e))
            pass


    '''
        根据股票代码（code）和日期（date）判断库中是否存在该股票
    '''
    # def isExistStock(self,code,date):
    #     sql = "SELECT * FROM " + self.table + " where code = '" + str(code) + "' and date = '" + str(date) +"'"
    #     n = self.dbOperator.execute(sql)
    #     # self.__logger.info(sql + " ,total:" + str(n))
    #     if n > 0:
    #         return True
    #     return False

    '''
        根据股票代码获取当前库中数据条数
    '''
    # def getCodeCount(self,code):
    #     sql = "SELECT code,date FROM " + self.table + " where code = '" + str(code) + "'"
    #     n = len(self.dbOperator.findBySQL(sql))
    #     return n


if __name__ == '__main__':
    try:
        socket.setdefaulttimeout(100)
        stock_list = ts.get_stock_basics()

        # 入库
        index = stock_list.index.size


        for i in range(0, index):
            # 获取股票代码
            code = stock_list.index.values[i]
            db_conn = DbConnection().create_connection_pool().connection()
            StockKLine(db_conn).get_his_data_todb(code)
    except Exception as e:
        print('download stock list basic to db failed >>> ' + str(e))
        pass