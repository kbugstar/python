#coding:utf-8
import Queue
import socket
import threading
import tushare as ts

import time

from stock.com.zw.db.connection_pool import DbConnection
from stock.com.zw.stock.kline import stock_kline
from stock.com.zw.stock.kline.stock_kline import StockKLine


class WorkManager(object):
    def __init__(self,work_num=1000,thread_num=2,work_content=[],func=None):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.func = func
        self.__init_work_queue(work_num,work_content)
        self.__init_thread_pool(thread_num)



    '''
        初始化线程
    '''
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))


    '''
        初始化工作队列
    '''
    def __init_work_queue(self,work_num,work_content):

        for i in range(work_num):
            self.add_job(self.func, work_content.index.values[i])



    '''
        添加一项工作入队
    '''
    def add_job(self,func,*args):
        self.work_queue.put((func,list(args)))


    '''
        等待所有线程运行完毕
    '''
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()


'''
    Work类是一个Python线程池，不断地从workQueue队列中获取需要执行的任务，执行之，并将结果写入到resultQueue中。这里的workQueue和resultQueue都是线程安全的，其内部对各个线程的操作做了互斥。当从workQueue中获取任务超时，则线程结束。
'''
class Work(threading.Thread):
    def __init__(self,work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                do,args = self.work_queue.get(block=False) #任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.task_done() #通知系统任务执行完毕
            except:
                break


'''
具体要做的任务
'''
def do_job(args):
    time.sleep(0.1) #模拟处理时间
    print '#########'+str(threading.active_count),threading.current_thread(),list(args)


if __name__ == '__main__':
    start = time.time()
    socket.setdefaulttimeout(100)
    stock_list = ts.get_stock_basics()
    index = stock_list.index.size
    db_conn = DbConnection().create_connection_pool().connection()
    func = StockKLine(db_conn).get_his_data_todb
    work_manager = WorkManager(index,2,stock_list,func)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time : %s" %(end-start)



'''

Work类是一个Python线程池，不断地从workQueue队列中获取需要执行的任务，执行之，并将结果写入到resultQueue中。这里的workQueue和resultQueue都是线程安全的，其内部对各个线程的操作做了互斥。当从workQueue中获取任务超时，则线程结束。

　　WorkerManager负责初始化Python线程池，提供将任务加入队列和获取结果的接口，并能等待所有任务完成。

　　在 Python 中使用线程时，这个模式是一种很常见的并且推荐使用的方式。具体工作步骤描述如下：

创建一个 Queue.Queue() 的实例，然后使用数据对它进行填充。
将经过填充数据的实例传递给线程类，后者是通过继承 threading.Thread 的方式创建的。
生成守护线程池。
每次从队列中取出一个项目，并使用该线程中的数据和 run 方法以执行相应的工作。
在完成这项工作之后，使用 queue.task_done() 函数向任务已经完成的队列发送一个信号。
对队列执行 join 操作，实际上意味着等到队列为空，再退出主程序。
　　在使用这个模式时需要注意一点：通过将守护线程设置为 true，将允许主线程或者程序仅在守护线程处于活动状态时才能够退出。这种方式创建了一种简单的方式以控制程序流程，因为在退出之前，您可以对队列执行 join 操作、或者等到队列为空。队列模块文档详细说明了实际的处理过程，请参见参考资料：

join()
保持阻塞状态，直到处理了队列中的所有项目为止。在将一个项目添加到该队列时，未完成的任务的总数就会增加。当使用者线程调用 task_done() 以表示检索了该项目、并完成了所有的工作时，那么未完成的任务的总数就会减少。当未完成的任务的总数减少到零时，join() 就会结束阻塞状态。

'''