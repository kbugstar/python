#coding:utf-8
#!/usr/bin/env python
# create table log ( logline varchar(300));
# grant all on pythondata.* to 'pyuser'@'localhost' identified by "pypasswd"
import socket
import threading

import tushare as ts

import MySQLdb
import os
import sys
from time import ctime
from threading import Thread
from Queue import Queue

num_thread = 10
queue = Queue()


def listDir(path):
    file_list = []
    for filename in os.listdir(path):
        file_list.append(os.path.join(path, filename))
    return file_list


def readFile(file):
    alllines = []
    i = 0
    for line in open(file):
        alllines.append(line)

    return alllines




def writeLinestoDb(q, queue):
    print q,threading.currentThread().getName(),threading.currentThread().isAlive()
    sql = insertsql = 'INSERT INTO stock_his_data(date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover,code) ' \
                                          'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    while True:
        content = queue.get()
        for (code,data) in content.items():
            # print code,data
            #网络获取历史数据条数
            index = data.index.size

            conn = MySQLdb.connect(host="localhost",port=3306, user="root", passwd="root", db="pystock")
            cur = conn.cursor()

            cur.execute("SELECT code,date FROM stock_his_data where code = '" + str(code) + "'")
            rows = cur.fetchall()
            count = 0
            if rows != None:
                count = len(rows)

            if index == count:
                print '[' + str(code) + '] 历史数据已存在，共【' + str(count) + '】条'
            else:
                # print(
                # '日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率')
                his_data = {}
                for i in range(0, index):
                    # 获取股票代码
                    his_data['code'] = code
                    # 获取日期
                    his_data['date'] = data.index.values[i]
                    # 获取股票信息
                    value = data.values[i]
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
                    if not isExistStock(cur,his_data['code'], his_data['date']):
                        insertIntoDB(cur, his_data)
                        # stock_dict.append(stock)

                cur.close()
                conn.commit()
                conn.close()
                queue.task_done()

                print '[' + str(code) + '] 历史数据新入库，共【' + str(index) + '】条'


                # for i in range(1,len(content)):
                #     # param.append(content[i])
                #     param = content[i].replace('\n','').split(',')
                #     param.append(001)
                #     cur.execute(sql, param)
                # cur.close()
                # conn.commit()
                # conn.close()
                # queue.task_done()

def isExistStock(cur, code, date):
    sql = "SELECT * FROM stock_his_data where code = '" + str(code) + "' and date = '" + str(date) + "'"
    n = cur.execute(sql)
    # self.__logger.info(sql + " ,total:" + str(n))
    if n > 0:
        return True
    return False


def insertIntoDB(cur,dict):

        sql = "insert into stock_his_data ("
        param = []
        for key in dict:
            sql += key + ','
            param.append(dict.get(key))
        param = tuple(param)
        sql = sql[:-1] + ") values("
        for i in range(len(dict)):
            sql += "%s,"
        sql = sql[:-1] + ")"

        # self.logger.debug(sql % param)
        n = cur.execute(sql, param)


def main():
    # print "Readfile Start at,", ctime()
    # for file in listDir('E:/py/stock/com/zw/stock/file/csv'):
    #     queue.put(readFile(file))
    # print "Readfile Done at,", ctime()
    # for q in range(num_thread):
    #     worker = Thread(target=writeLinestoDb, args=(q, queue))
    #     worker.setDaemon(True)
    #     worker.start()
    # print "Insert into mysql Main Thread at", ctime()
    # queue.join()
    # print "Insert into mysql at,", ctime()

    start = ctime()
    print "=============================get his data start at ", start
    try:
        socket.setdefaulttimeout(100)
        stock_list = ts.get_stock_basics()
        index = stock_list.index.size

        for i in range(index):
            code = stock_list.index.values[i]
            print "%s --- %s" %(i,code)
            data = {code:ts.get_hist_data(code)}
            queue.put(data)
        print "Readfile Done at,", ctime()
        for q in range(num_thread):
            worker = Thread(target=writeLinestoDb, args=(q, queue))
            print worker.getName(),worker.isAlive()

            worker.setDaemon(True)
            worker.start()
        queue.join()
    except Exception as e:
        print('download stock history data to db failed >>> ' + str(e))
        pass

    end = ctime()
    print "=============================get his data end at ", end
    print "=============================use total time ", end - start

if __name__ == "__main__":
    main()
