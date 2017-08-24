#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/21 0021 11:17:05
# @Author  : Aries
# @Site    : 
# @ File    : demo_m.py
# @Software: PyCharm Community Edition

import pandas as pd
import numpy as np


ser_obj = pd.Series(range(10,20))
#预览数据  预览前五行
# print(ser_obj.head(5))
# print(ser_obj)
# print(ser_obj * 2)  # 对value进行运算
# print(ser_obj > 15) # 取出
# print(ser_obj[ser_obj > 15])
#
# print(ser_obj.values)
# print(type(ser_obj.values))
# print(ser_obj.index)
# print(type(ser_obj.index))


# year_data = {2001:17.8,2002:20.1,2003:16.5}
# ser_obj2 = pd.Series(year_data)
# print(ser_obj2.head())
# print(ser_obj2.index)
#属性
# ser_obj2.name = 'temp'  # 指定真个Series的名称
# ser_obj2.index.name = 'year' # 指定索引列的名称
# print(ser_obj2.head())

# 通过ndarray构造DataFrame
# array = np.random.randn(5,4)
# print(array)

# df_obj = pd.DataFrame(array)
# print(df_obj.head())



dic_data = { 'A':1,
             'B':pd.Timestamp("20170410"),
             'C':pd.Series(1,index=list(range(4)),dtype='float32'),
             'D':np.array([3]*4,dtype='int32'),
             'E':pd.Categorical(["Python","Java","C++","C#"]),
             'F':'ChinaHadoop'
            }
# print(dic_data)
df_obj2 = pd.DataFrame(dic_data)
# print(df_obj2)
# print(df_obj2['A'])
# print(type(df_obj2['A'])) # <class 'pandas.core.series.Series'>
# print(df_obj2.A)
#增加列  G列为D列 +4
# df_obj2['G'] = df_obj2['D'] + 4
# print(df_obj2)
#删除列
# del(df_obj2['G'])
# print(df_obj2)

#索引切片
ser_obj = pd.Series(range(5),index=['a','b','c','d','e'])
print(ser_obj)
print(df_obj2)
# print(ser_obj[1:3]) #通过索引切片，留首不留尾
# print(ser_obj['a':'c']) #通过索引名称切片，留首留尾
#不连续索引
# print(ser_obj[[1,3]]) #通过索引切片
# print(ser_obj[['a','c']]) #通过索引名称切片，不连续


# 三种索引方式
# 1、 .loc  标签索引，标签名称索引，可以是字符串
#  Series
# print(ser_obj['b':'d'])
# print(ser_obj.loc['b':'d'])
#  DataFrame
# print(df_obj2['A'])
# print(df_obj2.loc[0:2,'A']) # 先取整个集合的0-2行（0:2是标签索引，所以包含第二行），再去A这一列

# 2、 .iloc  位置索引，i=int ，0/1/2/3...
# print(ser_obj[1:3])  # 位置索引，所以 1:3 留首不留尾
# print(ser_obj.iloc[1:3])  # 位置索引，所以 1:3 留首不留尾
# print(df_obj2.iloc[0:2,1])
# 3、 .ix  标签与位置混合索引，先按标签索引，如果标签不存在，再按位置索引
# print(ser_obj.ix[1:3])
# print(ser_obj.ix['a':'c'])
# print(df_obj2.ix[0:2,0])

# 注意：DataFrame索引时可将其看作ndarray操作
# 标签的切片索引是包含末尾位置的
