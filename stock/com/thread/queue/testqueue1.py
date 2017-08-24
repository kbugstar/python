#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 0012 15:58
# @Author  : Aries
# @Site    : 
# @File    : testqueue1.py
# @Software: PyCharm


#而对于慢速生产者和快速消费者而言，代码如下:




import Queue, threading, time, random


class consumer(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que

    def run(self):
        while True:
            item = self.queue.get()
            if item == None:
                break
                # processing the item
            print self.name, item
            self.queue.task_done()
        self.queue.task_done()
        return


que = Queue.Queue()

consumers = [consumer(que) for x in range(3)]
for c in consumers:
    c.start()
for x in range(10):
    item = random.random() * 10
    time.sleep(item)
    que.put(item, True, None)

que.put(None)
que.put(None)
que.put(None)
que.join()
import Queue, threading, time, random


class consumer(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que

    def run(self):
        while True:
            item = self.queue.get()
            if item == None:
                break
            # processing the item
            print self.name, item
            self.queue.task_done()
        self.queue.task_done()
        return


que = Queue.Queue()

consumers = [consumer(que) for x in range(3)]
for c in consumers:
    c.start()
for x in range(10):
    item = random.random() * 10
    time.sleep(item)
    que.put(item, True, None)

que.put(None)
que.put(None)
que.put(None)
que.join()

# 这种情况下，快速消费者在get时需要阻塞（否则返回了这线程就结束了～）因此对于停止整个程序，使用的是None标记，让子线程遇到None便返回结束。
#
# 因为消费速度大于产生速度，因此先运行子线程等待队列加入新的元素，然后再慢速地添加任务。
#
# 注意最后put（None）三次，是因为每个线程返回都会取出一个None，都要这样做才可以使三个线程全部停止。当然有种更简单粗暴的方法，就是把子线程设置为deamon，一但生产完成，开始que.join()
# 阻塞直至队列空就结束主线程，子线程虽然在阻塞等待队列也会因为deamon属性而被强制关闭。。。。
#
# 本文举了2个单一生产者多消费者的例子。参考资料是 < python参考手册 > 第三版，上面有单c和单p的代码。
#
# 有关多线程的函数如put，join什么的， 还是自己先看书学好概念吧～
#
# Queue的好处就在于它是线程安全的，只要理解多任务的的运行关系，加之明白阻塞的概念，就可以轻松地完成多种情况下的任务产生和处理机制。
#
# 不过协程也是种好的处理方法，以后再看看。。。。。。