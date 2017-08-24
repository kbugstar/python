#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/9 0009 18:56
# @Author  : Aries
# @Site    : 
# @File    : test01.py
# @Software: PyCharm
from numpy import *

print random.rand(4,4) # 构造一个4*4的随机数组

print '----------------------------------'

randMat = mat(random.rand(4,4))   # mat函数将数组转化成矩阵
print randMat.I