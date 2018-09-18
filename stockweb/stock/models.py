# coding:utf-8
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models

# Create your models here.


'''
    当天收盘价与最高价之后的最低价的比例
'''
class Current_Price_Of_Low_Rate(models.Model):
    code = models.CharField('股票代码',max_length=6)
    current_price = models.DecimalField('前价格（当日的收盘价）',max_digits=10,decimal_places=5)
    current_date = models.DateField('前价格（当日的收盘价）',default="")
    high_price = models.DecimalField('最高价',max_digits=10,decimal_places=5)
    high_date = models.DateField('最高价出现日期',default="")
    low_price = models.DecimalField('最低价',max_digits=10,decimal_places=5,default="")
    low_date = models.DateField('最低价出现日期',default="")
    rate = models.DecimalField('当前价与最高价的比值',max_digits=10,decimal_places=5)
    ave_price_up = models.BooleanField('均线是否成多头排列')
    volume_up = models.BooleanField('是否放量')
    turnover = models.DecimalField('换手率',max_digits=10,decimal_places=5,default="")

    # 为model加入字符串变现形式
    def __unicode__(self):
        return self.code



'''
    股票基本信息
'''
class Stock_Basics(models.Model):
    code = models.CharField('股票代码', max_length=6)
    name = models.CharField('名称', max_length=10)
    industry = models.CharField('所属行业', max_length=10)
    area = models.CharField('地区', max_length=10)
    pe = models.DecimalField('市盈率',max_digits=15,decimal_places=5,blank=True, null=True)
    outstanding = models.DecimalField('流通股本(亿)',max_digits=15,decimal_places=5,blank=True, null=True)
    totals = models.DecimalField('总股本(亿)',max_digits=15,decimal_places=5,blank=True, null=True)
    totalAssets = models.DecimalField('总资产(万)',max_digits=15,decimal_places=5,blank=True, null=True)
    liquidAssets = models.DecimalField('流动资产',max_digits=15,decimal_places=5,blank=True, null=True)
    fixedAssets = models.DecimalField('固定资产',max_digits=15,decimal_places=5,blank=True, null=True)
    reserved = models.DecimalField('公积金',max_digits=15,decimal_places=5,blank=True, null=True)
    reservedPerShare = models.DecimalField('每股公积金',max_digits=15,decimal_places=5,blank=True, null=True)
    esp = models.DecimalField('每股收益',max_digits=15,decimal_places=5,blank=True, null=True)
    bvps = models.DecimalField('每股净资',max_digits=15,decimal_places=5,blank=True, null=True)
    pb = models.DecimalField('市净率',max_digits=15,decimal_places=5,blank=True, null=True)
    timeToMarket = models.CharField('上市日期', max_length=8)
    undp = models.DecimalField('未分利润',max_digits=15,decimal_places=5,blank=True, null=True)
    perundp = models.DecimalField('每股未分配',max_digits=15,decimal_places=5,blank=True, null=True)
    rev = models.DecimalField('收入同比( %)',max_digits=15,decimal_places=5,blank=True, null=True)
    profit = models.DecimalField('利润同比( %)',max_digits=15,decimal_places=5,blank=True, null=True)
    gpr = models.DecimalField('毛利率( %)',max_digits=15,decimal_places=5,blank=True, null=True)
    npr = models.DecimalField('净利润率( %)',max_digits=15,decimal_places=5,blank=True, null=True)
    holders = models.FloatField('股东人数',default=0)

    # 为model加入字符串变现形式
    def __unicode__(self):
        return self.code





'''
    股票基本信息
'''
class Stock_Fenshi(models.Model):
    code = models.CharField('股票代码', max_length=6)
    date = models.DateField('日期')
    time = models.TimeField('时间')
    price = models.DecimalField('价格',max_digits=10,decimal_places=5,blank=True, null=True)
    change = models.DecimalField('价格变动',max_digits=10,decimal_places=5,blank=True, null=True)
    volume = models.IntegerField('成交量',default=0)
    amount = models.BigIntegerField('成交额',default=0)
    type = models.CharField('买卖类型',max_length=6,default='')

    # 为model加入字符串变现形式
    def __unicode__(self):
        return self.code
