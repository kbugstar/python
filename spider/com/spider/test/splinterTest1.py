# -*- coding: utf-8 -*-
from splinter.browser import Browser

b = Browser(driver_name="chrome")

b.visit("http://www.baidu.com")  ###注意不要去掉http://