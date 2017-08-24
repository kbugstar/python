#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/9 0009 17:12
# @Author  : Aries
# @Site    : 
# @File    : test1.py
# @Software: PyCharm
import socket
import urllib2

import re

import time
from BeautifulSoup import BeautifulSoup

time.sleep(1)


Accept = "image/gif,image/x-xbitmap,image/jpeg,image/pjpeg,*/*"         # 属性规定能够通过文件上传进行提交的文件类型。
AcceptLanguage = "zh-cn"                                                        # 支持的语言
UserAgent = "Mozilla/4.0 (compatible;MSIE 5.01; Windows NT 5.0"         #  浏览器标识 (操作系统标识; 加密等级标识; 浏览器语言) 渲染引擎标识 版本信息
AcceptEncoding = "*"                                                            # 压缩类型 支持所有类型 Accept-Encoding: compress;q=0.5, gzip;q=1.0//按顺序支持 gzip , compress
# 伪装成浏览器，容错
def get(url,data=None,headers = None,referer = None):
    request = urllib2.Request(url)
    if data:
        request.add_data(data)
    if headers:
        for key in headers.keys():
            request.add_header(key,headers[key])
    if not request.has_header("User-Agent"):
        request.add_header("User_Agent",UserAgent)
    if not request.has_header("Referer") and referer:
        request.add_header("Referer",referer)
    if not request.has_header("Accept"):
        request.add_header("Accept",Accept)
    if not request.has_header("Accept-Language"):
        request.add_header("Accept-Language",AcceptLanguage)
    if None and not request.has_header("Accept-Encoding"):
        request.add_header("Accept-Encoding",AcceptEncoding)

    method = request.get_method()
    try:
        result = urllib2.urlopen(request)
        return result
    except urllib2.URLError,error:
        print error
    except socket.error,error:
        print error
    except:
        pass
    return None





aaa=3640
url1 = "http://bbs.ustc.edu.cn/cgi/bbstdoc?board=PieBridge&start="
while aaa>0:
    aaa = aaa - 20
    aaa1 = str(aaa)
    url1 = url1+aaa1
    # fp = urllib2.urlopen(url1)          # 打开url
    fp = get(url1)
    try:
        s = fp.read().decode("gb2312",'ignore')   # 把上面操作结果赋给s  把gb2312修改成网页的编码
        # 在这里添加一段代码，修改网页内容s的编码设置
        s = re.sub("charset=gb2312","charset=utf-8",s,re.I)
        s = s.encode('utf-8','ignore')
    except:
        s = fp.read()
    soup = BeautifulSoup(s)             # 用beautifulSoup分析s
    polist = soup.findAll('span')      # 找出所有tag <span> 的内容
    print polist[0].contents[0]        # 打印出第一个tag<span>中间的内容





