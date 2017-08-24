#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from subprocess import Popen,PIPE

#         host='localhost',
#         port = 3306,
#         user='root',
#         passwd='7668150Tt00',
#         db ='sanguogame',

# CREATE TABLE `sanguogame`.`new_table` (
#   `id` INT NOT NULL AUTO_INCREMENT,
#   `name` VARCHAR(45) NOT NULL,
#   `class` VARCHAR(45) NOT NULL,
#   `age` VARCHAR(45) NOT NULL,
#     PRIMARY KEY (`id`, `name`));
from stock.com.zw.utils import logger_factory


class mysqlobj():
    def __init__(self,addr = 'localhost',port = 3306,usname = 'root',uspw = 'root',defDB = 'pystock'):
        self.logger = logger_factory.getLogger('DBOperator')
        self.mysqladdr = addr           #mysql地址
        self.mysqlport = port           #mysql端口
        self.mysqlusername = usname     #mysql登陆用户名
        self.mysqlpassword = uspw       #mysql登陆密码
        self.mysqlDefaleDB = defDB      #mysql默认登陆数据库
        self.connectManger = None       #mysql连接管理器
        self.mysqlcursor = None         #mysql消息收发器
        self._connectMysql()            #连接mysql数据库
    def _connectMysql(self):
        self.connectManger = MySQLdb.connect(
                                             host = self.mysqladdr,
                                             port = self.mysqlport,
                                             user = self.mysqlusername,
                                             passwd = self.mysqlpassword,
                                             db = self.mysqlDefaleDB,
                                             charset="utf8"
                                             )
        self.mysqlcursor = self.connectManger.cursor()
    #调用mysql命令
    def execute(self,cmdstr):
        if self.mysqlcursor:
            return self.mysqlcursor.execute(cmdstr)
        else:
            return -999#mysql 未连接
    def inPutDataWithSqlFile(self,sqlfilepath):
        process = Popen('/usr/local/mysql/bin/mysql -h%s -P%s -u%s -p%s %s'  %(self.mysqladdr, self.mysqlport, self.mysqlusername, self.mysqlpassword, self.mysqlDefaleDB), stdout=PIPE, stdin=PIPE, shell=True)
        output = process.communicate('source '+sqlfilepath)
        print output

    def findBySQL(self, sql):
        try:
            self.mysqlcursor.execute(sql)
            rows = self.mysqlcursor.fetchall()
            return rows
        except MySQLdb.Error, e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))