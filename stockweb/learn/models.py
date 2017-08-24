#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# 此模块都是与数据库相关的代码  支持sqlite3、mysql、postgresql

# 新建一个Person类，继承自models.Model，一个人有姓名和年龄，这里用了两种Field
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

    def __unicode__(self):
        # 在Python3中使用 def __str__(self)
        return self.name