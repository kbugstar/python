# -*- coding: utf-8 -*-
import urllib2
import re
from BeautifulSoup import BeautifulSoup
#
# aaa = 3640
#
# url = "http://bbs.ustc.edu.cn/cgi/bbstdoc?board=PieBridge&start="
# while aaa>0:
#     aaa = aaa-20
#     aaa1 = str(aaa)
#     url1 = url+aaa1
#     print(url1)
#     fp = urllib2.urlopen(url1)
#
#     try:
#         s = fp.read().decode("gb2312",'ignore')  #把gb2312修改成网页的编码
#         # print(unicode(s,'gb2312').encode('utf-8'))  #处理读取网页内容中的中文乱码
#         s = re.sub("charset=gb2312","charset=utf-8",s,re.I)
#         s = s.encode('utf-8','ignore')
#     except:
#         s = fp.read()
#
#     soup = BeautifulSoup(s)
#     polist = soup.findAll('span')
#     print(polist[0].contents[0]) #获取第一个span标签中的内容
#


if __name__=='__main__':
    for i in range(1,10):
        print i