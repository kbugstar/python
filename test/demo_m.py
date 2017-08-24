#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 0014 16:06:49
# @Author  : Aries
# @Site    : 
# @ File    : demo_m.py
# @Software: PyCharm Community Edition


def methon1(a, b):
    if a > b:
        print a - b
    else:
        print b - a


def methon2(a=None):
    if a == None:
        print 'a is None'
    else:
        print a


methon1(1,2)


# if __name__ == '__main__':
#     methon1(1,2)
#     methon2()