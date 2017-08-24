#!usr/bin/env python
# -*- coding: utf-8 -*-
import os

import shutil


def saveToFile(fileName,content,isOverwWrite):
    if(fileName.find('/')!=-1 or fileName.find('\\')!=-1): #包含目录
        #转义
        fileName.replace('\\','/')
        #最后一次出现/的位置
        lastindex =  fileName.rindex('/')
        #判断是否是文件
        lastCon = fileName[lastindex+1:len(fileName)]
        if(lastCon.find('.')!=-1):  #是文件
            dirPath = fileName[0:lastindex]
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            if not os.path.exists(fileName):
                with open(fileName, 'wb') as code:
                    code.write(content)
                    print '文件内容写入成功'
            else: #文件已存在
                if isOverwWrite: #覆盖
                    areainfo = open(fileName)
                    temp = areainfo.read()
                    if (temp == content):
                        return
                    with open(fileName, 'wb') as code:
                        code.write(content)
                        print '文件内容写入成功'
        else:  #传进来的是个目录
            print '未指定文件名，目录创建成功，内容未写入'
            os.makedirs(fileName)


if __name__ == '__main__':
    saveToFile('aaaa/aaa/aa/a.txt','aaa')