from config.bot_config import mysql_charset,mysql_password,mysql_db,mysql_host,mysql_user
import pymysql

class Database(object):
    def __init__(self):
        self.connection = pymysql.connect(host=mysql_host,user=mysql_user,password=mysql_password,db=mysql_db,charset=mysql_charset,cursorclass=pymysql.cursors.DictCursor,autocommit=True)
        self.cursor = self.connection.cursor()

    def executeWithReturn(self,command):
        self.reconnect()
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def executeWithCommit(self,command):
        self.reconnect()
        self.cursor.execute(command)

    def executeWithCount(self,command):
        self.reconnect()
        return self.cursor.execute(command)

    def reconnect(self):
        self.connection.ping(reconnect=True)
        self.executeWithCommit('sql')