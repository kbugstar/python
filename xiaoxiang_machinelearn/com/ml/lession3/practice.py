#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/9 0009 12:44:29
# @Author  : Aries
# @Site    : 
# @ File    : practice.py
# @Software: PyCharm Community Edition
import csv

data_path = "../../../files/ml/lession3/survey.csv"

def run_main():
    male_set = {"male","m"} # 男性可能的取值
    female_set = {"female","f"} # 女性可能的取值

    # 构造统计结果的数据结构 result_dict
    # 其中每个元素是键值对，键 是国家名称，值 是列表结构
    # 列表第一个数是国家女性统计数据，第二个是男性统计数据
    # 入 {'United States':[20,50],'Canada':[30,40]}
    # 思考：这里的值为什么用列表(list) 而不用元祖(tuple)
    result_dict = {}

    with open(data_path,'r',newline='') as csvfile:
        # 加载数据
        rows = csv.reader(csvfile)
        for i,row in enumerate(rows): # 对一个可循环的数据，每次返回循环次数和当前值
            if i==0:
                # 跳过第一行表头数据
                continue
            if i % 50 == 0:
                print('正在处理第{}行数据...'.format(i))
            # 性别数据
            gender_val = row[2]
            country_val = row[3]

            # 去掉可能存在的空格
            gender_val = gender_val.replace(' ','')
            # 转换为小写
            gender_val = gender_val.lower()

            # 判断“国家”是否已经存在
            if country_val not in result_dict:
                # 如果不存在，初始化数据
                result_dict[country_val] = [0,0]

            # 判断性别
            if gender_val in female_set:
                # 女性
                result_dict[country_val][0] += 1
            elif gender_val in male_set:
                # 男性
                result_dict[country_val][1] += 1
            else:
                # 噪声数据
                pass
    # 将结果写入文件
    with open('gender_country.csv','w',newline='',encoding='utf-16') as csvfile:
        csvwriter = csv.writer(csvfile,delimiter="，")
        # 写入表头
        csvwriter.writerow(['国家','男性','女性'])

        # 写入统计结果
        for k,v in list(result_dict.items()):
            csvwriter.writerow([k,v[0],v[1]])




if __name__ == "__main__":
    run_main()