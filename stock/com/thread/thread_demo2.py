#coding:utf-8
import Queue
import socket
import threading
import time
import tushare as ts
import urllib2

hosts = ["http://yahoo.com", "http://google.com","http://www.baidu.com"]
ids = [1,2,3,4,5,6,7,8,9,0,11,22,33,44,55,66,77,88,99,111,222,333,444,555,666,777,888,999]

# start = time.time()
# for host in hosts:
#     url = urllib2.urlopen(host)
#     print url.read(1024)
# print "Elapsed Time: %s" %(time.time()-start)

queue = Queue.Queue()  #创建队列
count = 0

class ThreadClass2(threading.Thread):
    def __init__(self,queue,count):
        threading.Thread.__init__(self)
        self.queue = queue #队列赋值
        self.count = count

    def run(self):
        while True:
            self.count = self.count+1
            code = self.queue.get()
            print self.count,threading.Thread.getName(self),code
            open(str(code)+'.txt','w')

            #告诉队列线程已经执行完毕
            self.queue.task_done()


start = time.time()
def main():
    socket.setdefaulttimeout(100)
    stock_list = ts.get_stock_basics()
    index = stock_list.index.size
    for i in range(index):
        queue.put(stock_list.index.values[i])

    #初始化线程池，并初始化线程队列
    for i in range(100):
        t = ThreadClass2(queue,count)
        #通过将守护线程设置为 true，将允许主线程或者程序仅在守护线程处于活动状态时才能够退出。这种方式创建了一种简单的方式以控制程序流程，因为在退出之前，您可以对队列执行 join 操作、或者等到队列为空。队列模块文档详细说明了实际的处理过程
        t.setDaemon(True)
        t.start()

#对队列执行 join 操作，实际上意味着等到队列为空，再退出主程序。
queue.join()

main()
print "Elapsed Time: %s" %(time.time()-start)