#!usr/bin/env python
# -*- coding:utf-8 -*-
import cookielib
import socket
import urllib2

import time

from com.spider.mhxy import zipUtils


def readCptcha(captchaUrl='http://xyq.cbg.163.com/cgi-bin/show_captcha.py'):
    # req = urllib2.Request(captchaUrl)  # req表示向服务器发送请求#
    # req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    # req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    # req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
    # req.add_header('Host', 'res.xyq.cbg.163.com')
    # req.add_header('Proxy-Connection', 'keep-alive')
    # req.add_header('Upgrade-Insecure-Requests', '1')
    # req.add_header('User-Agent',
    #                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
    # timeout = 20  #
    # socket.setdefaulttimeout(timeout)  # 设置socket默认超时时间，因为urlopen之后的read()操作其实是调用了socket层的某些函数
    # time.sleep(10)
    # response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response#
    # the_page = zipUtils.unzip(response.read())  # 用read解析获得的HTML文件#
    #
    # print the_page






    cookiejar = cookielib.CookieJar()
    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(urlopener)

    urlopener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'))
    urlopener.addheaders.append(('Accept-Encoding', 'gzip, deflate, sdch'))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8'))
    urlopener.addheaders.append(('Cache-Control','max-age=0'))
    urlopener.addheaders.append(('Connection', 'keep-alive'))
    urlopener.addheaders.append(('Cookie','sid=0001rwr60KUhC4X2x5l083rBD4iwA-UC8liH2Jw6DOi; _ntes_nnid=7afa07fb9513875209d9edcab6a270d3,1470815482984; _ntes_nuid=7afa07fb9513875209d9edcab6a270d3; fingerprint=2042963340; cbg_login_ck=000RmzWz4gB20EmyW2AA0bXXfe4z7Ol-rUEzZl3VGkD'))
    urlopener.addheaders.append(('Host', 'xyq.cbg.163.com'))
    urlopener.addheaders.append(('Upgrade-Insecure-Requests', '1'))
    urlopener.addheaders.append(('User-Agent',
                                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'))

    timeout = 20  #
    socket.setdefaulttimeout(timeout)  # 设置socket默认超时时间，因为urlopen之后的read()操作其实是调用了socket层的某些函数
    time.sleep(10)
    req = urllib2.Request(captchaUrl)  # req表示向服务器发送请求#
    response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response#
    the_page = response.read()  # 用read解析获得的HTML文件#

    sss = urlopener.open(captchaUrl).read()

    print the_page  # 在屏幕上显示出来#
    print sss


if __name__=='__main__':
    readCptcha()