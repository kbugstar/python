#coding:utf-8
import json
import os

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from stockweb import settings


class Learn():
    BASE_DIR = settings.BASE_DIR  # 项目目录
    # 假设图片放在static/pics/里面
    PICS = os.listdir(os.path.join(BASE_DIR, 'common_static/images'))

    print (PICS)  # 启动时终端上可以看到有哪些图片，我只放了一张，测试完后这一行可以删除

    def index(self,request):
        # return HttpResponse(u"STOCK ANALYSIS SYSTEM")
        # 跳转到应用 learn 下的 templates 目录下的 home.html 文件
        # 将应用，比如 learn 添加到stockweb 下的setting 中的 INSTALLED_APPS 下，使用 render时，Django会自动到 app 下的templates中找到文件
        # 小提示，DEBUG=True 的时候，Django 还可以自动找到 各 app 下 static 文件夹中的静态文件（js，css，图片等资源），方便开发

        # 向视图传递字符串
        string = u"测试输出字符串"

        # 向后台传递list
        list = ["HTML", "CSS", "jQuery", "Python", "Django"]

        # 向后台传递字典
        info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}

        # 一个长度为100的List
        list1 = map(str,range(100))
        list1 = []
        return render(request,'home.html',{'string':string,'list':list,'info_dict':info_dict,'list1':list1})

    def add(self,request):
        # a = request.GET['a']
        # b = request.GET['b']
        # request.GET 类似于一个字典，更好的办法是用 request.GET.get('a', 0) 当没有传递 a 的时候默认 a 为 0
        a = request.GET.get('a',0)
        b = request.GET.get('b',0)
        c = int(a) + int(b)
        return HttpResponse(str(c))


    def add2(request,a,b):
        print (a,b)
        c = int(a) + int(b)
        return HttpResponse(str(c))


    def ajax(self, request):
        return render(request, 'ajax_test.html', locals())


    def add(self, request):
        a = request.GET['a']
        b = request.GET['b']
        a = int(a)
        b = int(b)
        return HttpResponse(str(a + b))


    def ajax_list(self, request):
        a = range(100)
        return HttpResponse(json.dumps(a), content_type='application/json')

    def ajax_mlist(self, request):
        person_info_dict = [
            {"name": "xiaoming", "age": 20},
            {"name": "tuweizhong", "age": 24},
            {"name": "xiaoli", "age": 33},
        ]
        return HttpResponse(json.dumps(person_info_dict), content_type='application/json')


    def ajax_dict(self, request):
        name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
        return HttpResponse(json.dumps(name_dict), content_type='application/json')

    def get_pic(self,request):
        color = request.GET.get('color')
        number = request.GET.get('number')
        name = '{}_{}'.format(color, number)

        # 过滤出符合要求的图片，假设是以输入的开头的都返回
        result_list = filter(lambda x: x.startswith(name), self.PICS)

        print ('result_list', result_list)

        return HttpResponse(
            json.dumps(result_list),
            content_type='application/json')