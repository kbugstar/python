#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/10 0010 16:54
# @Author  : Aries
# @Site    : 
# @File    : tests.py
# @Software: PyCharm
import urllib2


def aaa(n):
    # try:
    #     print ('10','/',n,'=', 10/n)
    # except Exception as e:
    #     testExcettion(1)
    #     print (e)
    A0 = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))
    A1 = range(10)
    A2 = [i for i in A1 if i in A0]
    A3 = [A0[s] for s in A0]
    A4 = [i for i in A1 if i in A3]
    A5 = {i: i * i for i in A1}
    A6 = [[i, i * i] for i in A1]

    print(A0)
    print(A1)
    print(A2)
    print(A3)
    print(A4)
    print(A5)
    print(A6)

    for s in A0:
        print(s)



def getUrl():
    url = "http://www.baidu.com"
    res_data = urllib2.urlopen(url)
    res = res_data.read()
    print res




if __name__ == '__main__':
    for num in range(10, 20):
        for i in range(2, num):
            if num % i == 0:
                j = num / i
                print("%d等于%d*%d" % (num, i, j))
                break
        else:
            print("%d是一个质数" % num)