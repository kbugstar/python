#coding:utf-8
"""stockweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import time

import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf.urls import url
from django.contrib import admin

# 2.1.2
# from apscheduler.scheduler import Scheduler
from learn import views as learn_view
from scrapy.core.scheduler import Scheduler

from stock import views as stock_view
import logging


logging.basicConfig()


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 练习
    # url(r'^$', learn_view.index, name='home'),
    url(r'^add/$', learn_view.Learn().add, name='add'), #配置带参数的URL路径 http://localhost:8000/add/?a=5&b=9  前面地址配置必须以 /$ 结尾，否则会影响后面以 add...开头请求
    url(r'^add/(\d+)/(\d+)/$', learn_view.Learn().add2, name='add2'), #配置带参数的URL路径 http://localhost:8000/add/4/9/
    url(r'^new_add/(\d+)/(\d+)/$', learn_view.Learn().add2, name='add3'), #配置带参数的URL路径 http://localhost:8000/add/4/9/
    # ajax
    url(r'^ajax/$', learn_view.Learn().ajax,name='ajax'),
    url(r'^add/$', learn_view.Learn().add, name='add'),
    url(r'^ajax_list/$', learn_view.Learn().ajax_list, name='ajax-list'),
    url(r'^ajax_mlist/$', learn_view.Learn().ajax_mlist, name='ajax-mlist'),
    url(r'^ajax_dict/$', learn_view.Learn().ajax_dict, name='ajax-dict'),
    url(r'^get_pic/$', learn_view.Learn().get_pic, name='get-pic'),


    # stock 分析
    # url(r'^stock/$',stock_view.Stock().getCowStock,name='stock'),

    # 分页
    url(r'^stocklist/$', stock_view.Stock().showStockList,name='stocklist'),


]


# 2.1.2

# sched = Scheduler()

# @sched.interval_schedule(cron='0 56 13 ? * MON-FRI')
# def mytask():
#     stock_view.Stock().computer()
# sched.start()

from apscheduler.schedulers.blocking import BlockingScheduler
# def my_job():
#     print 'hello world'
# sched = BlockingScheduler()
# sched.add_job(my_job, 'interval', seconds=5)
# sched.start()



# timez = pytz.timezone("Asia/Shanghai")
# schedeler = BlockingScheduler()
# schedeler.add_job(stock_view.Stock().computer,'cron',  hour=16, minute=25, timezone=timez)
# try:
#     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     schedeler.start()
# except (KeyboardInterrupt,SystemExit):
#     print 'job execute error'
#     schedeler.shutdown()


timez = pytz.timezone("Asia/Shanghai")
schedule = BackgroundScheduler(timezone=timez)

schedule.add_job(stock_view.Stock().computer, 'cron',day_of_week='mon-fri', hour=7, minute=37)

# schedule.add_job(stock_view.Stock().computer, 'cron',day_of_week='mon-fri', hour='9-15', minute=39)

schedule.add_job(stock_view.Stock().download_stock_basic_info_todb, 'cron', day_of_week = 'mon-fri', hour=7, minute=36)

# schedule.add_job(stock_view.Stock().download_fenshi, 'cron',day_of_week='mon-fri', hour=16, minute=36)

# schedule.add_job(stock_view.Stock().download_fenshi_thread, 'cron',day_of_week='mon-fri', hour=18, minute=20)

try:
    schedule.start()
except Exception as e:
    print ('定时任务启动失败，异常：'+ str(e))