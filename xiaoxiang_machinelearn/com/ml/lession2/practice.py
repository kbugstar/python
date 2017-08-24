#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/3 0003 15:28:00
# @Author  : Aries
# @Site    : 
# @ File    : practice.py
# @Software: PyCharm Community Edition
import datetime
import numpy as np
import matplotlib .pyplot as plt


def is_convert_float(str):
    """
        判断一个字符串能否转换为float
    :param str: 
    :return: 
    """
    try:
        float(str)
    except:
        return False

    return True


def get_sum(str_array):
    """
        返回字符串数组中数字的综合
    :param str_array: 
    :return: 
    """
    # 去掉不能转出成数字的数据
    cleaned_data = filter(is_convert_float,str_array)
    # 转换数据类型
    float_array = np.array(cleaned_data,np.float)

    return np.sum(float_array)


def run_man():
    """
        main function
    """
    # 数据文件地址
    filename = "../../../files/ml/lession2/presidential_polls.csv"

    ## Step1. 列名预处理
    # 读取列名，即第一行数据
    with open(filename,'r') as f:
        col_names_str = f.readline()[:-1] # [:-1]表示不读取末尾换行符 '\n'

    # 将字符串拆分，并组成列表
    col_name_lst = col_names_str.split(',')
    print (col_name_lst)

    # 使用的列名
    # rawpoll_clinton 无加权规整的数据
    # adjpoll_clinton 加权规整的数据
    use_col_name_lst = ['enddate','rawpoll_clinton','rawpoll_trump','adjpoll_clinton', 'adjpoll_trump']

    # 获取相应列名的索引号
    use_col_index_lst = [col_name_lst.index(use_col_name) for use_col_name in use_col_name_lst]
    print (use_col_index_lst)

    ## Step2 读取数据
    data_array = np.loadtxt(filename,        # 文件名
                             delimiter=',',   # 分隔符
                             skiprows=1,       # 跳过第一行，即跳过列名
                             dtype=str,       # 数据类型
                             usecols=use_col_index_lst)  # 读取指定的列索引号
    print (data_array)

    ## Step3 数据处理
    # 处理日期格式数据
    enddate_idx = use_col_name_lst.index('enddate')
    enddate_lst = data_array[:,enddate_idx].tolist()  # 拿到所有行的 enddate 列的数据
    print (enddate_lst)
    # 将日期字符串格式统一，即 'yyyy/mm/dd'
    enddate_lst = [enddate.replace('-','/') for enddate in enddate_lst]
    print (enddate_lst)
    # 将日期字符串转换成日期
    # for enddate in enddate_lst:
    #     print(enddate)
    #     s = enddate.replace('b','')
    #     s = s.replace('\'','')
    #     print(s)
    #     date = datetime.datetime.strptime(s,"%m/%d/%Y")
    #     print(date)
    date_lst = [datetime.datetime.strptime(enddate.replace('b','').replace('\'',''),"%m/%d/%Y") for enddate in enddate_lst]
    print (date_lst)
    # 构造年份-月份列表
    month_lst = ['%d-%02d'%(date_obj.year,date_obj.month) for date_obj in date_lst]
    month_array = np.array(month_lst)
    months = np.unique(month_array)
    print(months)

    # Step4 数据分析
    # 统计民意投票数

    # cliton
    # 原始数据 rawpoll
    rawpoll_clinton_idx = use_col_name_lst.index('rawpoll_clinton')
    rawpoll_clinton_data = data_array[:,rawpoll_clinton_idx]
    # 调整后的数据 adjpoll
    adjpoll_clinton_idx = use_col_name_lst.index('adjpoll_clinton')
    adjpoll_clinton_data = data_array[:, adjpoll_clinton_idx]

    # trump
    # 原始数据
    rawpoll_trump_idx = use_col_name_lst.index('rawpoll_trump')
    rawpoll_trump_data = data_array[:, rawpoll_trump_idx]
    # 调整后的数据 adjpoll
    adjpoll_trump_idx = use_col_name_lst.index('adjpoll_trump')
    adjpoll_trump_data = data_array[:, adjpoll_trump_idx]

    # 结果保存
    results = []

    for month in months:
        # clinton
        # 原始数据
        rawpoll_clinton_month_data = rawpoll_clinton_data[month_array == month]
        # 统计当月的总票数
        rawpoll_clinton_month_sum = get_sum(rawpoll_clinton_month_data)
        # 调整后的adjpoll
        adjpoll_clinton_month_data = adjpoll_clinton_data[month_array == month]
        # 统计当月总票数
        adjpoll_clinton_month_sum = get_sum(adjpoll_clinton_month_data)

        # trump
        # 原始数据
        rawpoll_trump_month_data = rawpoll_trump_data[month_array == month]
        # 统计当月的总票数
        rawpoll_trump_month_sum = get_sum(rawpoll_trump_month_data)
        # 调整后的adjpoll
        adjpoll_trump_month_data = adjpoll_trump_data[month_array == month]
        # 统计当月总票数
        adjpoll_trump_month_sum = get_sum(adjpoll_trump_month_data)

        results.append((month,rawpoll_clinton_month_sum,adjpoll_clinton_month_sum,rawpoll_trump_month_sum,adjpoll_trump_month_sum))

    print (results)
    months,raw_clinton_sum,adj_clinton_sum,raw_trump_sum,adj_trump_sum = zip(*results)

    ## Step5 可视化分析结果
    fig, subplot_arr = plt.subplots(2,2,figsize=(15,10))

    # 原始数据趋势展示
    subplot_arr[0,0].plot(raw_clinton_sum,color='r')
    subplot_arr[0,0].plot(raw_trump_sum,color='g')

    width = 0.25
    x = np.arange(len(months))
    subplot_arr[0,1].bar(x,raw_clinton_sum,width,color='r')
    subplot_arr[0,1].bar(x+width,raw_trump_sum,width,color='g')
    subplot_arr[0,1].set_xticks(x+width)
    subplot_arr[0,1].set_xticklabels(months,rotation='vertical')

    # 调整数据趋势展示
    subplot_arr[1,0].plot(adj_clinton_sum,color='r')
    subplot_arr[1,0].plot(adj_trump_sum,color='g')

    subplot_arr[1, 1].bar(x, adj_clinton_sum, width, color='r')
    subplot_arr[1, 1].bar(x + width, adj_trump_sum, width, color='g')
    subplot_arr[1, 1].set_xticks(x + width)
    subplot_arr[1, 1].set_xticklabels(months, rotation='vertical')

    plt.subplots_adjust(wspace=0.2)
    plt.show()







if __name__=="__main__":
    run_man()