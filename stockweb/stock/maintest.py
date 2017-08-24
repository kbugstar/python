#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/20 0020 17:36
# @Author  : Aries
# @Site    : 
# @File    : maintest.py
# @Software: PyCharm


if __name__=='__main__':
    dic = {'000001':1.32,'20002':1.24,'60003':1.0,'60005':2.1}
    new_dic = {}
    l = sorted(dic.iteritems(), key=lambda d: d[1], reverse=False)
    for i in range(len(l)):
        if len(l[i])==2:
            new_dic[str(i)+'--'+l[i][0]] = l[i][1]

    for key in new_dic.keys():
        print new_dic.get(key)
    print new_dic