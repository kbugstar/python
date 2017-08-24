#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/13 0013 18:44:43
# @Author  : Aries
# @Site    : 
# @File    : train_demo.py
# @Software: PyCharm

import pandas as pd
import numpy as np
from pandas import Series,DataFrame


data_train = pd.read_csv("E:\\py\\xiaoxiang_machinelearn\\files\\titanic\\train.csv")

# 统计没条记录的没列的属性的总和，可以反映出什么属性数据缺失最多，比如此处的 Cabin
# data_train.info()


print data_train.describe()








'''
PassengerId => 乘客ID
Pclass => 乘客等级(1/2/3等舱位)
Name => 乘客姓名
Sex => 性别
Age => 年龄
SibSp => 堂兄弟/妹个数
Parch => 父母与小孩个数
Ticket => 船票信息
Fare => 票价
Cabin => 客舱
Embarked => 登船港口
'''