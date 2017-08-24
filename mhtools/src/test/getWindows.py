#coding=utf-8
'''
Created on 2016-5-26

@author: zhuwei
'''
import win32gui
import win32con
from pprint import pprint  
  
def gbk2utf8(s):  
    return s.decode('gbk').encode('utf-8')  
  
def show_window_attr(hWnd):  
    ''''' 
    显示窗口的属性 
    :return: 
    '''  
    if not hWnd:  
        return  
  
    #中文系统默认title是gb2312的编码  
    title = win32gui.GetWindowText(hWnd)  
    title = gbk2utf8(title)  
    clsname = win32gui.GetClassName(hWnd)  
    
    if "梦幻西游 ONLINE" in title:
        isMHXY = True
        #win32gui.MoveWindow(hWnd, 50, 50, win32con.SWP_NOSIZE, win32con.SWP_NOSIZE, True)
#        win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,win32con.SWP_DRAWFRAME)
  
  
        #窗口句柄:268124 
        #窗口标题:梦幻西游 ONLINE - (河南2区[牡丹亭] - 一休先生″[32716660])
        #窗口类名:MHXYMainFrame
    print '窗口句柄:%s ' % (hWnd)
    print '窗口标题:%s' % (title)
    print '窗口类名:%s' % (clsname)
    # print '窗口大小:%s' % (win32gui.)
    print ''
    
    
  
def show_windows(hWndList):  
    for h in hWndList:  
        show_window_attr(h)  
  
def demo_top_windows():  
    ''''' 
    演示如何列出所有的顶级窗口 
    :return: 
    '''  
    hWndList = []  
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)  
    show_windows(hWndList)  
  
    return hWndList  
  
def demo_child_windows(parent):  
    ''''' 
    演示如何列出所有的子窗口 
    :return: 
    '''  
    if not parent:  
        return  
  
    hWndChildList = []  
    win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd),  hWndChildList)  
    show_windows(hWndChildList)  
    return hWndChildList  
  
  
hWndList = demo_top_windows()  
assert len(hWndList)  
  
parent = hWndList[20]  
#这里系统的窗口好像不能直接遍历，不知道是否是权限的问题  
hWndChildList = demo_child_windows(parent)  
  
#print('-----top windows-----')
#pprint(hWndList)
  
#print('-----sub windows:from %s------' % (parent))
#pprint(hWndChildList)
