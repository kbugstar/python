#!usr/bin/env python
# -*- coding: utf-8 -*-
import random
import urllib2
import urllib
import cookielib
import zipUtils
from BeautifulSoup import BeautifulSoup


# -----------------------------------------------------------------------------
# Login in www.***.com.cn
from com.spider.mhxy import GetAreaInfo


def ChinaBiddingLogin(url, username, password):
    # Enable cookie support for urllib2
    cookiejar = cookielib.CookieJar()
    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    urllib2.install_opener(urlopener)

    urlopener.addheaders.append(('Referer',
                                 'http://xyq.cbg.163.com/cgi-bin/show_login.py?act=show_login&area_id=1&area_name=%E4%B8%8A%E6%B5%B71%E5%8C%BA&server_id=164&server_name=%E5%A4%A9%E9%A9%AC%E5%B1%B1'))
    urlopener.addheaders.append(
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'))
    urlopener.addheaders.append(('Accept-Encoding', 'gzip, deflate, sdch'))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8'))
    urlopener.addheaders.append(('Cache-Control', 'max-age=0'))
    urlopener.addheaders.append(('Connection', 'keep-alive'))
    urlopener.addheaders.append(('Host', 'xyq.cbg.163.com'))
    urlopener.addheaders.append(('Upgrade-Insecure-Requests', '1'))
    urlopener.addheaders.append(('User-Agent',
                                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'))

    print 'Login......' + url

    '''打开登陆页面'''
    req = urllib2.Request(url)  # req表示向服务器发送请求#
    response = urllib2.urlopen(req)  # response表示通过调用urlopen并传入req返回响应response#
    the_page = response.read()  # 用read解析获得的HTML文件#
    uzip = zipUtils.unzip(the_page).decode('gbk')
    print uzip  # 在屏幕上显示出来#

    # soup = BeautifulSoup(uzip)
    # print soup.find_all('img')



    '''下载并验证验证码图片'''
    imgurl = r'http://xyq.cbg.163.com/cgi-bin/show_captcha.py?stamp=' + str(random.random())
    DownloadFile(imgurl, urlopener)
    authcode = raw_input('Please enter the authcode:')







    '''打开中转页面'''
    loginUrl = 'http://xyq.cbg.163.com/cgi-bin/login.py'
    values = {"act": "do_anon_auth",
              "image_value": authcode,
              "server_id": "164",
              "server_name": "%E4%B8%8A%E6%B5%B71%E5%8C%BA",
              "next_url": "/cgi-bin/query.py?&amp;act=query&amp;server_id=164"}
    postData = urllib.urlencode(values)

    # 创建请求对象
    req = urllib2.Request(url=loginUrl, data=postData)
    # 获得服务器返回的数据
    response = urlopener.open(req)
    # 处理数据
    page = response.read()
    # 输出页面数据
    print(zipUtils.unzip(page).decode('gbk'))


    '''打开默认查询结果也没（不分种类）'''
    req1 = urllib2.Request(url='http://xyq.cbg.163.com/cgi-bin/query.py?&act=query&server_id=164')
    response1 = urllib2.urlopen(req1)  # response表示通过调用urlopen并传入req返回响应response#
    the_page1 = response1.read()  # 用read解析获得的HTML文件#
    uzip1 = zipUtils.unzip(the_page1).decode('gbk')
    print uzip1  # 在屏幕上显示出来#

    '''处理页面数据  获取出售列表table'''
    soup = BeautifulSoup(uzip1)
    print soup.findAll(id='soldList')

    return True
    # print BeautifulSoup(soup.findAll(id='soldList')).findAll('tr')


# -----------------------------------------------------------------------------
# Download from fileUrl then save to fileToSave
# Note: the fileUrl must be a valid file
def DownloadFile(fileUrl, urlopener):
    isDownOk = False

    try:
        if fileUrl:
            picture = urlopener.open(fileUrl).read()
            # 保存验证码到本地
            local = open('e:/code.jpg', 'wb')
            local.write(picture)
            local.close()

            isDownOK = True
        else:
            print 'ERROR: fileUrl is NULL!'
    except:
        isDownOK = False

    return isDownOK




# ------------------------------------------------------------------------------
def main():
    preUrl = 'http://xyq.cbg.163.com/cgi-bin/show_login.py?act=show_login'
    login_page = r'http://xyq.cbg.163.com/cgi-bin/show_login.py?act=show_login&area_id=1&area_name=%E4%B8%8A%E6%B5%B71%E5%8C%BA&server_id=164&server_name=%E5%A4%A9%E9%A9%AC%E5%B1%B1'
    areaUrlInfo = GetAreaInfo.getAreaInfo()
    print login_page
    for i in range(len(areaUrlInfo)):
        url = preUrl + areaUrlInfo[i]
        login_page = r''+url+''
        print login_page
        if ChinaBiddingLogin(login_page, '', ''):
            print '爬取数据成功......' + areaUrlInfo[i]
        else:
            print '爬取数据失败......' + areaUrlInfo[i]


# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()