#coding:utf-8
import threading

import datetime


class ThreadClass1(threading.Thread): #继承自 threading.Thread，也正因为如此，您需要定义一个 run 方法，以此执行您在该线程中要运行的代码
    def run(self):
        now = datetime.datetime.now()
        print "s% says Hello World at time: %s" %(self.getName(),now)



for i in range(2):
    t = ThreadClass1()
    t.start()