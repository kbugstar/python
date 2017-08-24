#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import json
import os
import socket
import threading
from cProfile import label

import types

import datetime
import tushare as ts
from time import ctime, time
from django.core.paginator import Paginator
from django.shortcuts import render

from com.zw.stock.tools.stock_tools import StockTools
from com.zw.utils.file_utils import FileUtils

from stock.models import Current_Price_Of_Low_Rate

from stock.com.zw.stock.thred.download_kline_thread import DownloadKlineThread

from stock.com.zw.utils.date_utils import DateUtils
from stock.models import Stock_Basics

from stockweb import settings
from stock.models import Stock_Fenshi

from stock.com.zw.stock.thred.download_fenshi_thread import DownloadFenShiThread


class Stock():

    '''
        分页查询方法
    '''
    # @ensure_csrf_cookie
    def showStockList(self,request):
        pagenum = request.GET.get('pagenum')
        pagesize = request.GET.get('pagesize')
        if pagenum==None or pagenum<1: pagenum=1
        if pagesize==None: pagesize=20

        code = request.GET.get('code')
        rateSort = request.GET.get('rateSort')
        turnover = request.GET.get('turnover')
        type = request.GET.get('type')
        if rateSort==None:
            rateSort = 'ASC'
        if turnover==None:
            turnover = 'ASC'
        if type==None:
            type = 'rate'

        queryset = Current_Price_Of_Low_Rate.objects.all()
        if code != u'None' and code != None and code != u'':
            if len(code) < 6:
                length = len(code)
                for i in range(0, 6 - length):
                    code = "0" + str(code)
            queryset = queryset.filter(code=code)
        else:
            code = ''  # 避免页面显示围 None

        if type=='rate':
            if rateSort=='ASC':
                queryset = queryset.order_by('rate')
                rateSort == 'DESC'
            else:
                queryset = queryset.order_by('-rate')
                rateSort == 'ASC'
        else:
            if turnover=='ASC':
                queryset = queryset.order_by('turnover')
                turnover == 'DESC'
            else:
                queryset = queryset.order_by('-turnover')
                turnover == 'ASC'
        p =  paging(Current_Price_Of_Low_Rate, pagenum, pagesize,queryset)
        return render(request, 'stocklist.html', locals())
        # print ' base dir %s' % BASE_DIR
        # print ' static dir %s' % STATIC_URL
        # per = request.session
        # username = per.get('username',u'访问')
        # if per.get('per_global',False) != '1':
        #     # create_db(username,'失败',u'访问前端更新记录页面，无权限' ,'系统平台','日志系统')
        #     return HttpResponseRedirect('404.html')
        # p = paging(Current_Price_Of_Low_Rate, pagenum, pagesize)

        # return render(request, 'stocklist.html', locals())








    '''
        （定时任务调用）
        下载并分析数据并入库
    '''
    def computer(self):
        path = settings.DOWNLOAD_PATH_KLINE
        path = 'E:/stock/csv/kline/'  # +str(DateUtils().get_current_date())+'/'
        print '=====================start ....' + str(ctime()) + '======================='

        print '开始下载股票历史K线数据......' + str(ctime())
        que = Queue.Queue()
        socket.setdefaulttimeout(100)
        # 获取股票代码列表
        stock_list = None

        try:
            stock_list = ts.get_stock_basics()
        except Exception as e:
            print 'get stock basics fail ' + '[ '+ str(e) +' ]'

        index = stock_list.index.size
        for i in range(0, index):
            # 获取股票代码
            code =  stock_list.index.values[i]
            que.put(code)

        # 多线程下载
        downloaders = [DownloadKlineThread(que,path) for x in range(4)]
        for download in downloaders:
            download.start()
        que.join()

        print '股票历史K线数据下载完成...' + str(ctime()) + '  共 [' + str(index) + '] 只'


        print '开始统计分析！ （' + str(ctime()) + '）'
        fu = FileUtils()
        content = {}
        files = fu.listDir(path)
        for file in files:
            code = file.split(".")[0][-6:]
            headers, data = fu.loadCsv(file)
            content[code] = data

        # 当前价格与该股最高价的比例
        currentPriceOfHighRate = StockTools().getCurrentPriceOfHighRate(content)
        currentPriceOfLowRateTrue, currentPriceOfLowRateFalse = StockTools().getCurrentPriceOfLowRate(content)
        # 对计算结果的比例进行排序，从小到大
        # sorted方法：参数1：获取dict的key、value，用于排序
        #           参数2：key指定用于排序的列：d:d[0]：表示用第一个元素排序，即key  d:d[1]：表示用第二个元素排序，即value
        #           参数3：reverse：是否进行反转，默认为False，默认排序从小到大，reverse=True表示从大到小排序
        currentPriceOfHighRate = sorted(currentPriceOfHighRate.iteritems(), key=lambda d: d[1], reverse=False)
        currentPriceOfLowRateTrue = sorted(currentPriceOfLowRateTrue.iteritems(), key=lambda d: d[1], reverse=False)
        currentPriceOfLowRateFalse = sorted(currentPriceOfLowRateFalse.iteritems(), key=lambda d: d[1], reverse=False)

        print currentPriceOfHighRate
        print currentPriceOfLowRateTrue
        print currentPriceOfLowRateFalse
        print '统计分析完成！（' + str(ctime()) + '）'





    '''
        下载股票信息到csv文件
    '''
    def download_stock_basic_info_tocsv(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            # self.__logger.info('begining download stock history data to csv! code = [' + str(code) + ']')
            if os.path.exists(path + str(DateUtils().get_current_date()) + '.csv'):
                return
            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()
            if type(stock_list) != types.NoneType:
                stock_list.to_csv(path + str(DateUtils().get_current_date()) + '.csv', encoding="utf_8_sig")
        except Exception as e:
            print(
                'download stock basics data failed!  Error = [' + str(e) + ']')


        '''
        下载股票信息并入库
        '''


    def download_stock_basic_info_todb(self):
        try:
            path = settings.DOWNLOAD_PATH_STOCKBASICS
            self.download_stock_basic_info_tocsv(path)

            socket.setdefaulttimeout(100)
            stock_list = ts.get_stock_basics()

            index = stock_list.index.size
            print(
            'code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket')
            stock = {}
            stock_dict = []
            for i in range(0, index):
                code = stock_list.index.values[i]

                exist = Stock_Basics.objects.filter(code = code)
                if len(exist) > 0:
                    continue

                sb = Stock_Basics()
                # # 获取股票代码
                # stock['code'] = stock_list.index.values[i]
                # # 获取股票信息
                # value = stock_list.values[i]
                # # 获取股票具体信息
                # stock['name'] = str(value[0]).decode(encoding='utf-8', errors='name解码错误,code=[' + stock['code'] + ']')
                # stock['industry'] = str(value[1]).decode(encoding='utf-8',
                #                                          errors='industry解码错误,code=[' + stock['code'] + ']')
                # stock['area'] = str(value[2]).decode(encoding='utf-8', errors='area解码错误,code=[' + stock['code'] + ']')
                # stock['pe'] = str(value[3])
                # stock['outstanding'] = str(value[4])
                # stock['totals'] = str(value[5])
                # stock['totalAssets'] = str(value[6])
                # stock['liquidAssets'] = str(value[7])
                # stock['fixedAssets'] = str(value[8])
                # stock['reserved'] = str(value[9])
                # stock['reservedPerShare'] = str(value[10])
                # stock['esp'] = str(value[11])
                # stock['bvps'] = str(value[12])
                # stock['pb'] = str(value[13])
                # stock['timeToMarket'] = str(value[14])
                #
                # stock['undp'] = str(value[15])
                # stock['perundp'] = str(value[16])
                # stock['rev'] = str(value[17])
                # stock['profit'] = str(value[18])
                # stock['gpr'] = str(value[19])
                # stock['npr'] = str(value[20])
                # stock['holders'] = str(value[21])

                # 获取股票代码
                sb.code = code
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

                sb.save()
        except Exception as e:
            print('download stock list basic to db failed >>> ' + str(e))
            pass



    def download_fenshi_tocsv(self,code,date,df):
        path = settings.DOWNLOAD_PATH_FENSHI
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            if os.path.exists(path + str(code)+'_'+str(date) + '.csv'):
                return

            df.to_csv(path + str(code)+'_'+str(date) + '.csv', encoding="utf_8_sig")
            print 'fenshi csv download successed !'

        except Exception as e:
            print(
                'download stock fenbi data to csv failed! code = [' + str(code) + '] , Error = [' + str(e) + ']')


    def download_fenshi_todb(self,code,date,df):

        try:
            index = df.index.size
            for i in range(0,index):
                value = df.values[i]
                sf = Stock_Fenshi()
                sf.code = code
                sf.date = date
                sf.time = value[0]
                sf.price = value[1]
                if value[2]=='--':
                    sf.change = 0
                else:
                    sf.change = value[2]
                sf.volume = value[3]
                sf.amount = value[4]
                sf.type = value[5]
                sf.save()
            print 'fenshi insert to db successed !  total ['+str(index)+']'
        except Exception as e:
            print(
                'download stock fenbi data to csv failed! code = [' + str(code) + '] , Error = [' + str(e) + ']')


    def download_fenshi(self):
        list = Stock_Basics.objects.all()


        for stock in list:
            n=0
            start = datetime.datetime.strptime(DateUtils().turn_date(stock.timeToMarket), '%Y-%m-%d')
            end = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')

            while start < end and n<730:
                n += 1
                print stock.code, end
                socket.setdefaulttimeout(100)
                try:
                    df = ts.get_tick_data(stock.code, end.date())
                    if type(df) != types.NoneType and df.index.size > 0 and 'alert' not in df.values[0][0]:
                        self.download_fenshi_tocsv(stock.code,end.date(),df)
                        self.download_fenshi_todb(stock.code,end.date(),df)
                    else:
                        print '       ----------no data'

                    end -= datetime.timedelta(days=1)
                except Exception as e:
                    print(
                        'get stock fenbi failed! code = [' + str(stock.code) + '] , Error = [' + str(
                            e) + ']')


    def download_fenshi_thread(self):
        list = Stock_Basics.objects.all()

        que = Queue.Queue()
        for stock in list:
            que.put(stock.code)

        # 多线程下载
        downloaders = [DownloadFenShiThread(que) for x in range(1)]
        for download in downloaders:
            download.start()

        que.join()





'''
    分页类
'''
class paging():
    '''
    此为文章分页功能，需要往里传递三个参数，分别如下：
    tablename:表名
    id:页码号，即第几页,这个一般从URL的GET中得到
    pagenum:每页显示多少条记录
    '''
    def __init__(self,tablename,id,pagenum,queryset=None):
        self.tablename = tablename
        self.page = int(id)
        self.pagenum = int(pagenum)
        if queryset ==None:
            queryset = self.tablename.objects.all().order_by('rate')          #查询tablename表中所有记录数，并以降序的方式对id进行排列
        self.p = Paginator(queryset,self.pagenum)                         #对表数据进行分页，每页显示pagenum条
        print self.p.object_list.query
        self.p_count = self.p.count                                 #数据库共多少条记录
        self.p_pages = self.p.num_pages                             #共可分成多少页
        self.p_content = self.p.page(self.page).object_list         #第N页的内容列表
        self.p_isprevious = self.p.page(self.page).has_previous()   #是否有上一页，返回True或False
        self.p_isnext = self.p.page(self.page).has_next()           #是否有下一页，返回True或False
        #获取上一页页码号,如果try报错，说明此页为最后一页，那就设置最后一页为1
        try:
            self.p_previous = self.p.page(self.page).previous_page_number()  #上一页页码号
        except:
            self.p_previous = '1'
        #获取下一页页码号,如果try报错，说明此页为最后一页，那就设置最后一页为self.p_pages
        try:
            self.p_next = self.p.page(self.page).next_page_number()
        except:
            self.p_next = self.p_pages
        #p_id获取当前页码，此变量是传递给模板用的，用于判断后，高亮当前页页码
        self.p_id = int(id)


    def p_range(self):
        '''
        获取页码列表
        当前页小于5时，取1-9页的列表
        最后页减当前页，小于5时，取最后9页的列表
        不属于以上2个规则的，则取当前页的前5和后4，共9页的列表
        '''
        # if self.page < 5:
        #     p_list = self.p.page_range[0:9]
        # elif int(int(self.p.num_pages) - self.page) < 5:
        #     p_list = self.p.page_range[-9:]
        # else:
        #     p_list = self.p.page_range[self.page-5:self.page+4]
        # return p_list
        if self.page < 5:
            p_list = list(self.p.page_range)[0:9]
        elif int(int(self.p.num_pages) - self.page) < 5:
            p_list = list(self.p.page_range)[-9:]
        else:
            p_list = list(self.p.page_range)[self.page-5:self.page+4]
        return p_list

