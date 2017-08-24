#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/20 0020 17:51
# @Author  : Aries
# @Site    : 
# @File    : collection_utils.py
# @Software: PyCharm

'''
    集合工具类
'''
class CollectionUtils():

    '''
        根据字典的值从小到大排序
    '''
    def sortDictByValue(self,dic):
        new_dic = {}

        l = sorted(dic.iteritems(), key=lambda d: d[1], reverse=False)
        s='00'
        for i in range(len(l)):
            if len(l[i]) == 2:
                if i<10:
                    s = str(0)+str(i)
                elif i<100:
                    s = str(i)
                new_dic[s+'--'+l[i][0]] = l[i][1]
        return new_dic