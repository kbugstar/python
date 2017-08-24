#coding:utf-8
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from learn.models import Ver_front

# from learn_models.settings import STATIC_URL
# from stockweb.stockweb.settings import BASE_DIR

'''
    p = paging(Ver_front,id,17) 中的Ver_front是数据库表名，id是当前页（url中传递过来的），17是指每页显示17条数据。就这么简单，后代码就搞定了分页的调用，剩下 的就是前端模板部分了。
'''



def show_version(request,id):
    # print ' base dir %s' % BASE_DIR
    # print ' static dir %s' % STATIC_URL
    # per = request.session
    # username = per.get('username',u'访问')
    # if per.get('per_global',False) != '1':
    #     # create_db(username,'失败',u'访问前端更新记录页面，无权限' ,'系统平台','日志系统')
    #     return HttpResponseRedirect('404.html')
    p = paging(Ver_front,id,17)
    # v1 = Ver_front(1,2,3,4,5)
    # v2 = Ver_front(1,2,3,4,5)
    # v3 = Ver_front(1,2,3,4,5)
    # v4 = Ver_front(1,2,3,4,5)
    # v5 = Ver_front(1,2,3,4,5)
    return render(request,'show_version.html',locals())





'''
    分页类
'''
class paging():
    '''
    此为文章分页功能，需要往里传递三个参数，分别如下：
    tablename:表名
    id:页码号，即第几页,这个一般从URL的GET中得到
    pagenum:每页显示多少条记录
    '''
    def __init__(self,tablename,id,pagenum):
        self.tablename = tablename
        self.page = int(id)
        self.pagenum = int(pagenum)
        tn = self.tablename.objects.all().order_by('-id')           #查询tablename表中所有记录数，并以降序的方式对id进行排列
        self.p = Paginator(tn,self.pagenum)                         #对表数据进行分页，每页显示pagenum条
        self.p_count = self.p.count                                 #数据库共多少条记录
        self.p_pages = self.p.num_pages                             #共可分成多少页
        self.p_content = self.p.page(self.page).object_list         #第N页的内容列表
        self.p_isprevious = self.p.page(self.page).has_previous()   #是否有上一页，返回True或False
        self.p_isnext = self.p.page(self.page).has_next()           #是否有下一页，返回True或False
        #获取上一页页码号,如果try报错，说明此页为最后一页，那就设置最后一页为1
        try:
            self.p_previous = self.p.page(self.page).previous_page_number()  #上一页页码号
        except:
            self.p_previous = '1'
        #获取下一页页码号,如果try报错，说明此页为最后一页，那就设置最后一页为self.p_pages
        try:
            self.p_next = self.p.page(self.page).next_page_number()
        except:
            self.p_next = self.p_pages
        #p_id获取当前页码，此变量是传递给模板用的，用于判断后，高亮当前页页码
        self.p_id = int(id)


    def p_range(self):
        '''
        获取页码列表
        当前页小于5时，取1-9页的列表
        最后页减当前页，小于5时，取最后9页的列表
        不属于以上2个规则的，则取当前页的前5和后4，共9页的列表
        '''
        # if self.page < 5:
        #     p_list = self.p.page_range[0:9]
        # elif int(int(self.p.num_pages) - self.page) < 5:
        #     p_list = self.p.page_range[-9:]
        # else:
        #     p_list = self.p.page_range[self.page-5:self.page+4]
        # return p_list
        if self.page < 5:
            p_list = list(self.p.page_range)[0:9]
        elif int(int(self.p.num_pages) - self.page) < 5:
            p_list = list(self.p.page_range)[-9:]
        else:
            p_list = list(self.p.page_range)[self.page-5:self.page+4]
        return p_list