#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/12 0012 15:56
# @Author  : Aries
# @Site    : 
# @File    : testqueue.py
# @Software: PyCharm
# 说实话这是我第二次接触多线程……第一次是java，不过java强大的对象思想让我有点小晕……所以python看得倒有些想法。
#
# 以下是一些基本观点和概念：
#
# 1.
# 多线程采用的是分时复用技术，即不存在真正的多线程，cpu做的事是快速地切换线程，以达到类似同步运行的目的，因为高密集运算方面多线程是没有用的，但是对于存在延迟的情况（延迟IO，网络等）多线程可以大大减少等待时间，避免不必要的浪费。
#
# 2.
# 原子操作：这件事情是不可再分的，如变量的赋值，不可能一个线程在赋值，到一半切到另外一个线程工作去了……但是一些数据结构的操作，如栈的push什么的，并非是原子操作，比如要经过栈顶指针上移、赋值、计数器加1等等，在其中的任何一步中断，切换到另一线程再操作这个栈时，就会产生严重的问题，因此要使用锁来避免这样的情况。比如加锁后的push操作就可以认为是原子的了……
#
# 3.
# 阻塞：所谓的阻塞，就是这个线程等待，一直到可以运行为止。最简单的例子就是一线程原子操作下，其它线程都是阻塞状态，这是微观的情况。对于宏观的情况，比如服务器等待用户连接，如果始终没有连接，那么这个线程就在阻塞状态。同理，最简单的input语句，在等待输入时也是阻塞状态。
#
# 4.
# 在创建线程后，执行p.start()，这个函数是非阻塞的，即主线程会继续执行以后的指令，相当于主线程和子线程都并行地执行。所以非阻塞的函数立刻返回值的～






#
# 对于资源，加锁是个重要的环节。因为python原生的list, dict等，都是not
# thread
# safe的。而Queue，是线程安全的，因此在满足使用条件下，建议使用队列。
#
# 队列适用于 “生产者 - 消费者”模型。双方无论数量多少，产生速度有何差异，都可以使用queue。
#
# 先来个例子：




import Queue, threading, time, random


class consumer(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que

    def run(self):
        while True:
            if self.queue.empty():
                break
            item = self.queue.get()
            # processing the item
            time.sleep(item)
            print self.name, item
            self.queue.task_done()
        return


que = Queue.Queue()
for x in range(10):
    que.put(random.random() * 10, True, None)
consumers = [consumer(que) for x in range(3)]

for c in consumers:
    c.start()
que.join()
import Queue, threading, time, random


class consumer(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.daemon = False
        self.queue = que

    def run(self):
        while True:
            if self.queue.empty():
                break
            item = self.queue.get()
            # processing the item
            time.sleep(item)
            print self.name, item
            self.queue.task_done()
        return


que = Queue.Queue()
for x in range(10):
    que.put(random.random() * 10, True, None)
consumers = [consumer(que) for x in range(3)]

for c in consumers:
    c.start()
que.join()

# 代码的功能是产生10个随机数（0～10
# 范围），sleep相应时间后输出数字和线程名称
#
# 这段代码里，是一个快速生产者（产生10个随机数），3
# 个慢速消费者的情况。
#
# 在这种情况下，先让三个consumers跑起来，然后主线程用que.join()
# 阻塞。
#
# 当三个线程发现队列都空时，各自的run函数返回，三个线程结束。同时主线程的阻塞打开，全部程序结束。
#

