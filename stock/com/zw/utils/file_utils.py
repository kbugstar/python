#coding:utf-8
import csv
import os

from stockweb.stock.com.zw.utils.date_utils import DateUtils

"""
    文件操作类
"""
class FileUtils():

    """
        文件列表，传入路径，返回该路径下的所有文件名称列表
        @:param path 文件
    """
    def listDir(self,path):
        file_list = []
        for filename in os.listdir(path):
            file_list.append(os.path.join(path, filename))
        return file_list


    """
        读取文件内容，按行读取
        @:param file 文件路径
    """
    def readFile(self,file):
        alllines = []
        for line in open(file):
            alllines.append(line)

        return alllines


    """
        加载csv文件
        @:param path 文件路径
        @:return headers 文件头
                 content 文件内容
    """
    def loadCsv(self,path):
        with open(path) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            content = []
            for row in f_csv:
                # print(row)
                content.append(row)
            return headers,content


if __name__=='__main__':
    fo = FileUtils()
    path = '/tmp/stock/csv/fenshi/' + str(DateUtils().get_current_date()) + '/'
    fileList = fo.listDir(path)
    headers = None
    content = {}
    for file in fileList:
        code = file.split('/')[6][:6]
        headers,data = fo.loadCsv(file)
        content[code] = data
    print(content)

