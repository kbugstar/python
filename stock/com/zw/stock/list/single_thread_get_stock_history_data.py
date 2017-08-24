# -*- coding:UTF-8 -*-

import urllib2
from stock.com.zw.db import db_operator

'''
    调用yahoo接口单线程获取股票历史数据
    采用雅虎的接口：http://ichart.yahoo.com/table.csv?s=<string>&a=<int>&b=<int>&c=<int>&d=<int>&e=<int>&f=<int>&g=d&ignore=.csv
    参 数：s — 股票名称
           a — 起始时间，月
           b — 起始时间，日
           c — 起始时间，年
           d — 结束时间，月
           e — 结束时间，日
           f — 结束时间，年
           g— 时间周期。
          （一定注意月份参数，其值比真实数据-1。如需要9月数据，则写为08。）
    示例 查询浦发银行2010.09.25 – 2010.10.8之间日线数据
    http://ichart.yahoo.com/table.csv?s=600000.SS&a=08&b=25&c=2010&d=09&e=8&f=2010&g=d
  返回：
     Date,Open,High,Low,Close,Volume,Adj Close
    2010-09-30,12.37,12.99,12.32,12.95,76420500,12.95
    2010-09-29,12.20,12.69,12.12,12.48,79916400,12.48
    2010-09-28,12.92,12.92,12.57,12.58,63988100,12.58
    2010-09-27,13.00,13.02,12.89,12.94,43203600,12.94
'''


dbOperator =db_operator.DBoperator()
table = "stock_quote_yahoo"
'''查找指定日期股票流量'''


def isStockExitsInDate(table, stock, date):
    sql = "select * from " + table + " where code = '%d' and date='%s'" % (stock, date)
    n = dbOperator.execute(sql)
    if n >= 1:
        return True


def getHistoryStockData(code, dataurl):
    try:
        r = urllib2.Request(dataurl)
        try:
            stdout = urllib2.urlopen(r, data=None, timeout=3)
        except Exception, e:
            print ">>>>>> Exception: " + str(e) + " code:" + code + " dataurl:" + dataurl
            return None

        stdoutInfo = stdout.read().decode('gbk').encode('utf-8')
        tempData = stdoutInfo.replace('"', '')
        stockQuotes = []
        if tempData.find('404') != -1:  stockQuotes = tempData.split("\n")

        stockDetail = {}
        for stockQuote in stockQuotes:
            stockInfo = stockQuote.split(",")
            if len(stockInfo) == 7 and stockInfo[0] != 'Date':
                if not isStockExitsInDate(table, code, stockInfo[0]):
                    stockDetail["date"] = stockInfo[0]
                    stockDetail["open"] = stockInfo[1]  # 开盘
                    stockDetail["high"] = stockInfo[2]  # 最高
                    stockDetail["low"] = stockInfo[3]  # 最低
                    stockDetail["close"] = stockInfo[4]  # 收盘
                    stockDetail["volume"] = stockInfo[5]  # 交易量
                    stockDetail["adj_close"] = stockInfo[6]  # 收盘adj价格
                    stockDetail["code"] = code  # 代码
                    dbOperator.insertIntoDB(table, stockDetail)
        result = tempData
    except Exception as err:
        print ">>>>>> Exception: " + str(err) + " code:" + code + " dataurl:" + dataurl
    else:
        return result
    finally:
        None


def get_stock_history():
    # 沪市2005-2015历史数据
    for code in range(601999, 602100):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%d.SS&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print getHistoryStockData(code, dataUrl)

    # 深市2005-2015历史数据
    for code in range(1, 1999):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%06d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print getHistoryStockData(code, dataUrl)

    # 中小板股票
    for code in range(2001, 2999):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%06d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print getHistoryStockData(code, dataUrl)

    # 创业板股票
    for code in range(300001, 300400):
        dataUrl = "http://ichart.yahoo.com/table.csv?s=%d.SZ&a=01&b=01&c=2005&d=01&e=01&f=2015&g=d" % code
        print getHistoryStockData(code, dataUrl)


def main():
    "main function"

    dbOperator.connDB()
    get_stock_history()
    dbOperator.closeDB()


if __name__ == '__main__':
    main()