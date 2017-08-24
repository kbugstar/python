#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/21 0021 11:17:05
# @Author  : Aries
# @Site    : 
# @ File    : demo_m.py
# @Software: PyCharm Community Edition


import pandas as pd
import numpy as np


########### apply和applymap方法
# df = pd.DataFrame(np.random.randn(5,4) -1)
# print(df)
# print(np.abs(df)) #求绝对值

#使用apply应用行货列数据
# f = lambda x : x.max()  相当于下面的函数   print(df.apply(lambda x : x.max()))
# def f(x):  # 求最大值
#     return x.max()
# print(df.apply(f)) #输出每一行的最大值


######## 排序
# s4 = pd.Series(range(10,15),index=np.random.randint(5,size=5))
# print(s4)
#索引排序  参数：ascending=False 降序排序
# print(s4.sort_index())
#值排序
# print(s4.sort_values)


####### pandas 数据处理
# 判断是否存在缺失值 isnull()
# 丢弃缺失数据（整行）  dropna
# 填充缺失数据 fillna


########  pandas 统计计算
# sum/mean/max/min...
# axis=0 按列   axis=1 按行
# skipna 排除缺失值，默认为True
# idmax/idmin/cumsum
# 统计描述：  describe 产生多个统计数据
# df_obj = pd.DataFrame(np.random.randn(5,4),columns=['a','b','c','d'])
# print(df_obj)
# print(df_obj.sum())
# print(df_obj.max())
# print(df_obj.min(axis=1))
# print(df_obj.describe())



########  pandas层级索引
# ser_obj = pd.Series(np.random.randn(12),
#                     index=[['a','a','a','b','b','b','c','c','c','d','d','d'],[0,1,2,0,1,2,0,1,2,0,1,2]])
# print(ser_obj)
# print(ser_obj['c']) # 外层索引，打印 c0  c1  c2
# print(ser_obj[:,'1']) # 内层索引，打印 a/b/c 对应的内层1
# 交换分成排序
# print(ser_obj.swaplevel())
#交换并排序分成
# print(ser_obj.swaplevel().sortlevel())



######### pandas分组与聚合
# 分组运算，经过三步：split -> apply -> combine
# 拆分：进行分组的根据
# 应用：每个分组运算的计算规则
# 合并：把每个分组的计算结果合并起来

# 分组
## 按列名分组  obj.groupby('label1')
## 按列名多层分组 obj.groupby(['label1','label2'])
## 按自定义的key分组 obj.groupby(self_def_key) 自定义的key可为列表或多层列表
## unstack可以将多层索引的结果转换成单层的dataframe

# GroupBy对象
# dic_obj = {'key1':['a','b','a','b','a','b','a','b'],
#            'key2':['one','one','two','three','two','two','one','three'],
#            'data1':np.random.randn(8),
#            'data2':np.random.randn(8)}
# df_obj = pd.DataFrame(dic_obj)
# print(df_obj)
# print(type(df_obj.groupby('key1')))  # <class 'pandas.core.groupby.DataFrameGroupBy'>
# print(df_obj.groupby('key1')) # 无任何输出内容，只是在内存中的位置
# print(df_obj['data1'].groupby(df_obj['key1'])) #对data1中的数据，依据key1进行排序，将key的值放入集合中，

# 分组运算
# grouped1 = df_obj.groupby('key1') # 依据key1分组，只有a/b两组
# print(grouped1.mean()) # 求均值运算
# print(grouped1.size()) # 该组的数据个数

# grouped2 = df_obj['data1'].groupby(df_obj['key1']) #只对data1的数据，依据key1进行分组
# print(grouped2.mean())
# print(grouped2.size())

# GroupBy对象可以迭代
# for name,data in grouped1:
#     print(name)
#     print(data)
#----------------------------------------------------------------------------
# 通过函数分组
# df_obj3 = pd.DataFrame(np.random.randint(1,10,(5,5)),
#                        columns=['a','b','c','d','e'],
#                        index=['AA','BBB','CC','D','EE'])
# print(df_obj3)

# def group_key(idx):
#     '''
#     :param idx: 为列索引或行索引
#     :return:
#     '''
#     return len(idx)
# print(df_obj3.groupby(group_key).size()) # 按索引的长度分组
# 以上自定义函数等价于 df_obj3.groupby(len).size()

#----------------------------------------------------------------------------
# 聚合  在分组的基础上进行运算  数组产生标量的过程，如mean()、count()等
'''
dict_obj = {'key1' : ['a','b','a','b','a','b','a','a'],
            'key2' : ['one','one','two','three','two','two','one','three',],
            'data1' : np.random.randint(1,10,8),
            'data2' : np.random.randint(1,10,8)}
df_obj5 = pd.DataFrame(dict_obj)
print(df_obj5)
'''
#内置聚合函数
# print(df_obj5.groupby('key1').sum()) #非NA值的和
# print(df_obj5.groupby('key1').max()) #非NA值的最大值
# print(df_obj5.groupby('key1').min()) #非NA值的最小值
# print(df_obj5.groupby('key1').size())
# print(df_obj5.groupby('key1').count()) # 分组中非NA值的数量
# print(df_obj5.groupby('key1').mean()) # 非NA值的平均值
# print(df_obj5.groupby('key1').describe())
# print(df_obj5.groupby('key1').median()) # 非NA值的算术中位数
# print(df_obj5.groupby('key1').prod()) # 非NA值积
# print(df_obj5.groupby('key1').first()) # 第一个非NA值（last：最后一个）
# print(df_obj5.groupby('key1').std()) # 无偏（分母为n-1）标准差（var:方差）
#自定义聚合函数
"""
def peak_range(df):
    '''
    :param df: 
    :return: 返回数值范围 
    '''
    return df.max() - df.min()

print(df_obj5.groupby('key1').agg(peak_range))
# 应用多个聚合函数
print(df_obj5.groupby('key1').agg(['mean','std','count',peak_range]))
# 使用transform
k1_sum_tf = df_obj5.groupby('key1').transform(np.sum).add_prefix('sum_')
# print(k1_sum_tf)
df_obj5[k1_sum_tf.columns] = k1_sum_tf
print(df_obj5)
"""

#-----------------------------------------------------------------------------------
# 数据连接
'''
    根据单个或多个键将不同的DataFrame的行链接起来，类比数据库链接操作，默认将重贴列的列名作为“外键”进行连接
    on：显示指定外键
    left_on：左侧数据的外键
    right_on：右侧数据的外键
    默认是“内连接（inner）”，即结果中的键是交集
    指定连接方式：
        “外连接”（outer），结果中的键是并集
        “左连接”（left）
        “右连接”（right）
    处理重复列名：
        suffixes，默认为_x，_y
    按索引连接：
        left_index = True 或 right_index=True
'''
'''
df_obj1 = pd.DataFrame({'key':['b','b','a','c','a','a','b'], 'data1':np.random.randint(0,10,7)})
df_obj2 = pd.DataFrame({'key':['a','b','d'], 'data2':np.random.randint(0,10,3)})
print(df_obj1)
print(df_obj2)
# print(pd.merge(df_obj1,df_obj2)) #内连接  默认根据相同的列名 key 进行连接
df_obj1 = df_obj1.rename(columns={'key':'key1'})
df_obj2 = df_obj2.rename(columns={'key':'key2'})
print(pd.merge(df_obj1,df_obj2,left_on='key1',right_on='key2'))  # 指定列关联
'''



#-------------------------------------------------------------------------------
# 重构
'''
stack
    将列索引旋转为行索引，完成层级索引
    DataFrame -> Series
unstack
    将层级索引展开
    Series -> DataFrame
    默认操作内层索引，即level=-1
'''
'''
df_obj1 = pd.DataFrame({'key':['b','b','a','c','a','a','b'], 'data1':np.random.randint(0,10,7)})
print(df_obj1)
print(df_obj1.stack())
print(df_obj1.unstack())
'''


#------------------------------------------------------------------------------
# 处理重复数据
'''
duplicated() 返回布尔型Series表示每行是否为重复行
drop_duplicates() 过滤重复行
    默认判断全部列
    可指定按某些列判断
map
    series根据map传入的函数对每行或每列进行转换
数据替换
    replace
'''



#-------------------------------------------------------------------------------
# 聚类模型：K-Means
