#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html)  #读取网页源码

print bsObj

#通过样式筛选元素
nameList = bsObj.findAll("span",{"class":"green"})
for name in nameList:
    print(name.getText())

#通过标签列表获取元素
tagObj = bsObj.findAll({"h1","h2","h3","h4","h5","h6"})
for tag in tagObj:
    print(tag.getText())

#通过文本匹配
textObj = bsObj.findAll(text="Anna Pavlovna")
print textObj