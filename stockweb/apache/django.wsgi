#coding=utf-8
 
import os
import sys
import django.core.handlers.wsgi
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'stockweb.settings'
app_apth = "E:/py/stockweb"
sys.path.append(app_apth)
application = django.core.handlers.wsgi.WSGIHandler()