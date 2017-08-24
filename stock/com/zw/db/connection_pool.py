#-*- coding: UTF-8 -*-

 # create db connection  pool

from DBUtils import PooledDB
import MySQLdb
import string

class DbConnection(object):
    def __init__(self):
        self.maxconn = 30        #最大连接数
        self.mincached = 10      #最小空闲连接
        self.maxcached = 20      #最大空闲连接
        self.maxshared = 30      #最大共享连接
        self.connstring = "root#root#127.0.0.1#3306#pystock#utf8"    #数据库连接地址
        self.dbtype = "mysql"    #数据库为MySQL



    def create_connection_pool (self,connstring=None,dbtype=None):
        if connstring == None:
            connstring = self.connstring
        if dbtype == None:
            dbtype = self.dbtype
        db_conn = connstring.split("#")
        if dbtype == 'mysql':
            try:
                pool = PooledDB.PooledDB(MySQLdb,user = db_conn[0],passwd = db_conn[1],host = db_conn[2],port = string.atoi(db_conn[3]),db=db_conn[4],charset = db_conn[5],mincached = self.mincached,maxcached = self.maxcached,maxshared = self.maxshared,maxconnections = self.maxconn)
                return pool
            except Exception,e:
                raise Exception,'conn datasource Excepts , %s !!! (%s).'%(db_conn[2],str(e))


if __name__=='__main__':
    c =    DbConnection().create_connection_pool().connection().cursor()
    print c