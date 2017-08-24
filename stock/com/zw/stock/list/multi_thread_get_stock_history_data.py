# -*- coding:UTF-8 -*-

import time
import threading


from stock.com.zw.db import db_operator
from stock.com.zw.utils import logger_factory
import urllib2


'''
A：实时价格数据采用腾讯的接口：沪市：http://qt.gtimg.cn/q=sh<int>，深市：http://qt.gtimg.cn/q=sz<int>
      如获取平安银行的股票实时数据：http://qt.gtimg.cn/q=sz000001，会返回一个包含股票数据的字符串：
      v_sz000001="51~平安银行~000001~11.27~11.27~11.30~316703~151512~165192~11.27~93~11.26~
      4352~11.25~4996~11.24~1037~11.23~1801~11.28~1181~11.29~2108~11.30~1075~11.31~1592~11.32~
      1118~15:00:24/11.27/3146/S/3545407/17948|14:56:59/11.26/15/S/16890/17787|
      14:56:56/11.25/404/S/454693/17783|14:56:54/11.26/173/B/194674/17780|14:56:51
      /11.26/306/B/344526/17777|14:56:47/11.26/16/B/18016/17773~
      20151029150142~0.00~0.00~11.36~11.25~
      11.26/313557/354285045~
      316703~35783~0.27~7.38~~11.36~11.25~0.98~1330.32~1612.59~1.03~12.40~10.14~";
      数据比较多，比较有用的是：1-名称；2-代码；3-价格；4-昨日收盘；5-今日开盘；6-交易量（手）；7-外盘；8-内盘；9-买一；10-买一量；11-买二；12-买二量；13-买三；14-买三量；15-买四；16-买四量；17-买五；18-买五量；19-卖一；20-卖一量；21-卖二；22-卖二量；23-卖三；24-卖三量；25-卖四；26-卖四量；27-卖五；28-卖五量；30-时间；31-涨跌；32-涨跌率；33-最高价；34-最低价；35-成交量（万）；38-换手率；39-市盈率；42-振幅；43-流通市值；44-总市值；45-市净率

B：现金流数据仍然采用腾讯接口：沪市：http://qt.gtimg.cn/q=ff_sh<int>，深市：http://qt.gtimg.cn/q=ff_sz<int>
      例如平安银行的现金流数据http://qt.gtimg.cn/q=ff_sz000001：
      v_ff_sz000001="sz000001~21162.20~24136.40~-2974.20~-8.31~14620.87~11646.65~2974.22~
      8.31~35783.07~261502.0~261158.3~平安银行~20151029~20151028^37054.20^39358.20~
      20151027^39713.50^42230.70~20151026^82000.80^83689.90~20151023^81571.30^71743.10";
      比较重要的：1-主力流入；2-主力流出；3-主力净流量；4-主力流入/主力总资金；5-散户流入；6-散户流出；7-散户净流量；8-散户流入/散户总资金；9-总资金流量；12-名字；13-日期


    上证编码：'600001' .. '602100'
    深圳编码：'000001' .. '001999'
    中小板：'002001' .. '002999'
    创业板：'300001' .. '300400'
'''



class StockTencent(object):
    # 数据库表
    __stockTables = {'cash': 'stock_cash_tencent', 'quotation': 'stock_quotation_tencent'}
    '''初始化'''

    def __init__(self):
        self.__logger = logger_factory.getLogger('StockTencent')
        self.__dbOperator = db_operator.DBoperator()

    def main(self):
        self.__dbOperator.connDB()
        threading.Thread(target=self.getStockCash()).start()
        threading.Thread(target=self.getStockQuotation()).start()
        self.__dbOperator.closeDB()

    '''查找指定日期股票流量'''

    def __isStockExitsInDate(self, table, stock, date):
        sql = "select * from " + table + " where code = '%s' and date='%s'" % (stock, date)
        n = self.__dbOperator.execute(sql)
        if n >= 1:
            return True

    '''获取股票资金流明细'''

    def __getStockCashDetail(self, dataUrl):
        # 读取数据
        tempData = self.__getDataFromUrl(dataUrl)

        if tempData == None:
            time.sleep(10)
            tempData = self.__getDataFromUrl(dataUrl)
            return False

        # 解析资金流向数据
        stockCash = {}
        stockInfo = tempData.split('~')
        if len(stockInfo) < 13: return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') == -1:
            table = self.__stockTables['cash']
            code = stockInfo[0].split('=')[1][2:]
            date = stockInfo[13]
            if not self.__isStockExitsInDate(table, code, date):
                stockCash['code'] = stockInfo[0].split('=')[1][2:]
                stockCash['main_in_cash'] = stockInfo[1]
                stockCash['main_out_cash'] = stockInfo[2]
                stockCash['main_net_cash'] = stockInfo[3]
                stockCash['main_net_rate'] = stockInfo[4]
                stockCash['private_in_cash'] = stockInfo[5]
                stockCash['private_out_cash'] = stockInfo[6]
                stockCash['private_net_cash'] = stockInfo[7]
                stockCash['private_net_rate'] = stockInfo[8]
                stockCash['total_cash'] = stockInfo[9]
                stockCash['name'] = stockInfo[12].decode('utf8')
                stockCash['date'] = stockInfo[13]
                # 插入数据库
                self.__dbOperator.insertIntoDB(table, stockCash)

    '''获取股票交易信息明细'''

    def getStockQuotationDetail(self, dataUrl):
        tempData = self.__getDataFromUrl(dataUrl)

        if tempData == None:
            time.sleep(10)
            tempData = self.__getDataFromUrl(dataUrl)
            return False

        stockQuotation = {}
        stockInfo = tempData.split('~')
        if len(stockInfo) < 45: return
        if len(stockInfo) != 0 and stockInfo[0].find('pv_none') == -1 and stockInfo[3].find('0.00') == -1:
            table = self.__stockTables['quotation']
            code = stockInfo[2]
            date = stockInfo[30]
            if not self.__isStockExitsInDate(table, code, date):
                stockQuotation['code'] = stockInfo[2]
                stockQuotation['name'] = stockInfo[1].decode('utf8')
                stockQuotation['price'] = stockInfo[3]
                stockQuotation['yesterday_close'] = stockInfo[4]
                stockQuotation['today_open'] = stockInfo[5]
                stockQuotation['volume'] = stockInfo[6]
                stockQuotation['outer_sell'] = stockInfo[7]
                stockQuotation['inner_buy'] = stockInfo[8]
                stockQuotation['buy_one'] = stockInfo[9]
                stockQuotation['buy_one_volume'] = stockInfo[10]
                stockQuotation['buy_two'] = stockInfo[11]
                stockQuotation['buy_two_volume'] = stockInfo[12]
                stockQuotation['buy_three'] = stockInfo[13]
                stockQuotation['buy_three_volume'] = stockInfo[14]
                stockQuotation['buy_four'] = stockInfo[15]
                stockQuotation['buy_four_volume'] = stockInfo[16]
                stockQuotation['buy_five'] = stockInfo[17]
                stockQuotation['buy_five_volume'] = stockInfo[18]
                stockQuotation['sell_one'] = stockInfo[19]
                stockQuotation['sell_one_volume'] = stockInfo[20]
                stockQuotation['sell_two'] = stockInfo[22]
                stockQuotation['sell_two_volume'] = stockInfo[22]
                stockQuotation['sell_three'] = stockInfo[23]
                stockQuotation['sell_three_volume'] = stockInfo[24]
                stockQuotation['sell_four'] = stockInfo[25]
                stockQuotation['sell_four_volume'] = stockInfo[26]
                stockQuotation['sell_five'] = stockInfo[27]
                stockQuotation['sell_five_volume'] = stockInfo[28]
                stockQuotation['datetime'] = stockInfo[30]
                stockQuotation['updown'] = stockInfo[31]
                stockQuotation['updown_rate'] = stockInfo[32]
                stockQuotation['heighest_price'] = stockInfo[33]
                stockQuotation['lowest_price'] = stockInfo[34]
                stockQuotation['volume_amout'] = stockInfo[35].split('/')[2]
                stockQuotation['turnover_rate'] = stockInfo[38]
                stockQuotation['pe_rate'] = stockInfo[39]
                stockQuotation['viberation_rate'] = stockInfo[42]
                stockQuotation['circulated_stock'] = stockInfo[43]
                stockQuotation['total_stock'] = stockInfo[44]
                stockQuotation['pb_rate'] = stockInfo[45]
                self.__dbOperator.insertIntoDB(table, stockQuotation)

    '''读取信息'''

    def __getDataFromUrl(self, dataUrl):
        r = urllib2.Request(dataUrl)
        try:
            stdout = urllib2.urlopen(r, data=None, timeout=3)
        except Exception, e:
            self.__logger.error(">>>>>> Exception: " + str(e))
            return None

        stdoutInfo = stdout.read().decode('gbk').encode('utf-8')
        tempData = stdoutInfo.replace('"', '')
        self.__logger.debug(tempData)
        return tempData

    '''获取股票现金流量'''

    def getStockCash(self):
        self.__logger.debug("开始:收集股票现金流信息")
        try:
            # 沪市股票
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=ff_sh%d" % code
                self.__getStockCashDetail(dataUrl)

                # 深市股票
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)

                # 中小板股票
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%06d" % code
                self.__getStockCashDetail(dataUrl)

                # '300001' .. '300400'
            # 创业板股票
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=ff_sz%d" % code
                self.__getStockCashDetail(dataUrl)

        except Exception as err:
            self.__logger.error(">>>>>> Exception: " + str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("结束：股票现金流收集")

    '''获取股票交易行情数据'''

    def getStockQuotation(self):
        self.__logger.debug("开始:收集股票交易行情数据")
        try:
            # 沪市股票
            for code in range(600001, 602100):
                dataUrl = "http://qt.gtimg.cn/q=sh%d" % code
                self.getStockQuotationDetail(dataUrl)

                # 深市股票
            for code in range(1, 1999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)

                # 中小板股票
            for code in range(2001, 2999):
                dataUrl = "http://qt.gtimg.cn/q=sz%06d" % code
                self.getStockQuotationDetail(dataUrl)

                # '300001' .. '300400'
            #  创业板股票
            for code in range(300001, 300400):
                dataUrl = "http://qt.gtimg.cn/q=sz%d" % code
                self.getStockQuotationDetail(dataUrl)

        except Exception as err:
            self.__logger.error(">>>>>> Exception: " + str(code) + " " + str(err))
        finally:
            None
        self.__logger.debug("结束:收集股票交易行情数据")


if __name__ == '__main__':
    StockTencent().main()