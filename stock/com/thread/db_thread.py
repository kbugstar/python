import MySQLdb, threading


class DataSource(object):
    def __init__(self, conf={'db_server':'127.0.0.1','port':3306,'db_user':'root','db_passwd':'root','db_name':'pystock','db_unicode':'true','db_charset':'utf8'}):
        self.conf = conf
        self.tl = threading.local()
        pass

    def __getConn__(self):
        if (not hasattr(self.tl, "conn")) or (self.tl.conn.open != 1):
            conf = self.conf
            conn = MySQLdb.connect(host=conf['db_server'],
                                   port=conf['port'],
                                   user=conf['db_user'],
                                   passwd=conf['db_passwd'],
                                   db=conf['db_name'],
                                   use_unicode=conf['db_unicode'],
                                   charset=conf['db_charset'])
            self.tl.conn = conn

        return self.tl.conn

    def getData(self, sql):
        conn = self.__getConn__()
        cur = conn.cursor()
        cur.execute(sql)
        ls = list(cur.fetchall())
        return ls

    def executeSql(self, sql):
        conn = self.__getConn__()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        pass


if __name__=='__main__':
    sql = "select * from stock_his_data"
    res = DataSource().getData(sql)
    print res