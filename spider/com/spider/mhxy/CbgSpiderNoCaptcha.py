#! usr/bin/env python
#-*- coding:utf-8 -*-
import cookielib
import urllib
import urllib2

from com.spider.mhxy import GetAreaInfo
from com.spider.mhxy import zipUtils


def cbg_spider(base_url,area_id,area_name,server_id,server_name):
    cookiejar = cookielib.CookieJar()
    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(urlopener)

    # urlopener.addheaders.append(('Referer','http://xyq.cbg.163.com/cgi-bin/show_login.py?act=show_login&area_id=1&area_name=%E4%B8%8A%E6%B5%B71%E5%8C%BA&server_id=164&server_name=%E5%A4%A9%E9%A9%AC%E5%B1%B1'))
    urlopener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'))
    urlopener.addheaders.append(('Accept-Encoding', 'gzip, deflate, sdch'))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8'))
    urlopener.addheaders.append(('Cache-Control', 'max-age=0'))
    urlopener.addheaders.append(('Connection', 'keep-alive'))
    urlopener.addheaders.append(('Host', 'xyq.cbg.163.com'))
    urlopener.addheaders.append(('Upgrade-Insecure-Requests', '1'))
    urlopener.addheaders.append(('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'))

    print 'connecting......' + server_name + ' - ' + area_name

    values = {
                "act": "query",
                "server_id": area_id,
            }

    query_data = urllib.urlencode(values)
    '''打开登陆页面'''
    req = urllib2.Request(url=base_url,data=query_data)  # req表示向服务器发送请求#
    response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response 第一次请求到中转页
    response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response 第二次才请求到数据页
    the_page = response.read()  # 用read解析获得的HTML文件#
    uzip = zipUtils.unzip(the_page).decode('gbk')
    print uzip  # 在屏幕上显示出来#



if __name__ == '__main__':
    base_url = 'http://xyq.cbg.163.com/cgi-bin/query.py'  # ?&act=query&
    area_info = GetAreaInfo.getAreaInfo()
    for area in area_info:
        area_id = area.split('&')[1].split('=')[1]
        area_name = area.split('&')[2].split('=')[1]
        server_id = area.split('&')[3].split('=')[1]
        server_name = area.split('&')[4].split('=')[1]
        cbg_spider(base_url,area_id,area_name,server_id,server_name)