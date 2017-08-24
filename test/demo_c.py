#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 0014 16:06:49
# @Author  : Aries
# @Site    : 
# @ File    : demo_m.py
# @Software: PyCharm Community Edition

class DemoClass:

    def methon1(self,a, b):
        if a > b:
            print a - b
        else:
            print b - a

    def methon2(self,a=None):
        if a == None:
            print 'a is None'
        else:
            print a

# DemoClass().methon1(1,2)
# DemoClass().methon2()