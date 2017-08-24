#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/14 0014 17:00:35
# @Author  : Aries
# @Site    : 
# @ File    : demo_area.py
# @Software: PyCharm Community Edition

from demo_const import PI

def calc_rount_area(radius):
    return PI * (radius ** 2)


def main():
    print "round area: ",calc_rount_area(2)


main()