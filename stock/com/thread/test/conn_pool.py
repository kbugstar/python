#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mysql连接线程池，初始化时设置3个连接池,连接池保持使用率小于80%，如果连接池使用率大于等于80%时则自动增加mysql连接量直到使用率小于80%，连接池最大50个
import socket
import threading
import time
import tushare as ts
from Queue import Queue

from stock.com.thread.test.db_operator import mysqlobj

_CONNECTTOOL = None


def requestComplete(n):
    _CONNECTTOOL.requestComplete(n)


class _connectThread(threading.Thread):
    def __init__(self, t_name, requstqueue, responeQueue, signal, ptime=3):
        threading.Thread.__init__(self, name=t_name)
        self.signal = signal  # 线程条件锁
        self.mysqlobj = mysqlobj()
        self.threadFunc = None  # mysql调用返回值
        self.requstqueue = requstqueue  # mysql请求列队
        self.responeQueue = responeQueue  # mysql返回列队
        self.timer = 0  # 超时定时器
        self.account = ''  # 作数据库mysql请求的帐号
        self.askType = 1  # 1.线程空闲，可以接受请求,2.正在发送数据库请求，等待返回结果,3.数据库结果已返回或请求超时，正在处理请求结果
        self.connectobj = None  # 当前请求连接数据对象
        self.conncetTimer = ptime  # 默认请求3秒无返回，则认为数据库请求超时

    def _setNewConnect(self, newobj):
        self.askType = 2
        self.timer = time.time()  # 开始发送mysql请求时间
        self.connectobj = newobj  # 接收mysqly请求数据对象
        self._sendRequest()

    def _sendRequest(self):
        if self.connectobj.backfunc != None:
            print 'thname=%s\n' % (self.getName())
            time.sleep(4)
            self.connectobj.cmdstr =  self.mysqlobj.findBySQL(self.connectobj.cmdstr)
            print '##############   %s,%s' %(self.account,self.connectobj.cmdstr)
            self.askType = 3
            self.responeQueue.put(self.connectobj)
            self.connectobj.comfunc(int(self.getName()))
            self.askType = 1

    def run(self):
        while (True):
            if self.askType == 1 and (not self.requstqueue.empty()):  # 线程是否空闲，请求队列中是否有请求对象
                objtmp = self.requstqueue.get()
                self._setNewConnect(objtmp)
            else:  # 没有数据请求，线程进入等待唤醒模式
                print 'thread wait:%s\n' % (self.getName())
                self.signal.clear()
                self.signal.wait()  # 请求结束等待下一次请求来唤醒


class _askObj():
    def __init__(self, account, cmdstr, backfunc,
                 ptype='sreach'):  # inset,del,update,sreach,分别为增加数据，删除数据，修改数据，查找数据,backfunc为查找到的数据返回
        self.account = account
        self.cmdstr = cmdstr
        self.ptype = ptype  # 数据库请求类型
        self.backfunc = backfunc  # 数据库请求返回回调函数
        self.outtimer = time.time()  # 数据库查找时间，用作查找超时处理,现在定义默认查找5秒未返回就超时，
        self.threadname = ''
        self.comfunc = requestComplete


class mysqlConnectThreads():
    def __init__(self, maxcon=50, mincon=3, addpencent=80):
        self.maxcon = maxcon
        self.mincon = mincon
        self.singal = threading.Event()
        self.addpencent = addpencent
        self.concount = 0  # 当前已连接mysql数量
        self.conthreads = {}
        self.singals = {}
        self.runthread = []
        self.waitthread = []
        self.threadCount = 0
        self.conpencent = 0.0  # 当前线程池使用率
        self.requestQueue = Queue()  # mysql请求列队
        self.responeQueue = Queue()  # mysql返回列队
        self._createConncets()

    # 初始化mysql连接池
    def _createConncets(self):
        global _CONNECTTOOL
        _CONNECTTOOL = self
        self.singals['1'] = threading.Event()
        self.conthreads['1'] = _connectThread('1', self.requestQueue, self.responeQueue, self.singals['1'])
        self.conthreads['1'].setDaemon(True)
        self.conthreads['1'].start()
        self.singals['2'] = threading.Event()
        self.conthreads['2'] = _connectThread('2', self.requestQueue, self.responeQueue, self.singals['2'])
        self.conthreads['2'].setDaemon(True)
        self.conthreads['2'].start()
        self.singals['3'] = threading.Event()
        self.conthreads['3'] = _connectThread('3', self.requestQueue, self.responeQueue, self.singals['3'])
        self.conthreads['3'].setDaemon(True)
        self.conthreads['3'].start()
        self.threadCount = 3
        self.waitthread = [1, 2, 3]

    # 使用线程池中线程发送mysql命令
    def mysqlexecute(self, account, cmdstr, backfunc, ptype='sreach'):
        reqtmp = _askObj(account, cmdstr, backfunc, ptype)
        self.requestQueue.put(reqtmp)
        qs = self.requestQueue.qsize()
        self.conpencent = (float)(qs / len(self.conthreads))
        print 'qs=%d\n' % (qs)
        if self.conpencent >= 0.8 and self.threadCount < self.maxcon:
            self.threadCount += 1
            self.singals[str(self.threadCount)] = threading.Event()
            self.conthreads[str(self.threadCount)] = _connectThread(str(self.threadCount), self.requestQueue,
                                                                    self.responeQueue,
                                                                    self.singals[str(self.threadCount)])
            self.conthreads[str(self.threadCount)].setDaemon(True)
            self.conthreads[str(self.threadCount)].start()
        print 'thread count:%d\n' % (self.threadCount)
        if len(self.waitthread) > 0:
            n = self.waitthread.pop()
            self.runthread.append(n)
            self.singals[str(n)].set()

    def requestComplete(self, n):
        if not self.responeQueue.empty():
            print 'requestComplete'
            reqtmp = self.responeQueue.get()
            reqtmp.backfunc(reqtmp.account, reqtmp.cmdstr)
        self.waitthread.append(n)


def asktest(backaccount, backdat):
    print 'asktest:%s,%s' % (backaccount, backdat)


# classtest
if __name__ == '__main__':
    con = mysqlConnectThreads()
    #获取股票列表
    socket.setdefaulttimeout(100)
    stock_list = ts.get_stock_basics()
    index = stock_list.index.size

    for i in range(index):
        # con.mysqlexecute(str(i)+'--'+str(stock_list.index.values[i]),"select count(*) from stock_his_data where code = '"+str(stock_list.index.values[i])+"'", asktest)
        con.mysqlexecute(str(i)+'--'+str(600019),"select * from stock_his_data where code = '"+str(600019)+"'", asktest)


    # ac = 1
    # while (True):
    #     ac += 1
    #     con.mysqlexecute(str(ac), 'select * from stock_his_data' + str(ac), asktest)
    #     time.sleep(1)