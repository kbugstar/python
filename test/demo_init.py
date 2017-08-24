#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/16 0016 11:39:13
# @Author  : Aries
# @Site    : 
# @ File    : demo_init.py
# @Software: PyCharm Community Edition


class Demo:

    def __init__(self,name,age):
        print 'this is init method '
        self.name = name
        self.age = age

    def __del__(self):
        print 'this is del method '

    def hello(self):
        print self.name
        print self.age

Demo("zs",15).hello()