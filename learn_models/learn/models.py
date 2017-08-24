#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ver_front(models.Model):
    # def __init__(self,id,item,flash,bin,status,dtime):
    #     self.id = id
    #     self.item = item
    #     self.flash = flash
    #     self.bin = bin
    #     self.status = status
    #     self.dtime = dtime
    #
    # id = models.IntegerField(primary_key=True)
    item = models.CharField(max_length=50)
    flash = models.CharField(max_length=50)
    bin = models.CharField(max_length=50)
    status = models.CharField(max_length=2)
    dtime = models.CharField(max_length=50)