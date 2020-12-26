from config.bot_config import mysql_charset,mysql_password,mysql_db,mysql_host,mysql_user
import pymysql

class Database(object):
    def __init__(self):
        self.connection = pymysql.connect(host=mysql_host,user=mysql_user,password=mysql_password,db=mysql_db,charset=mysql_charset,cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def databaseInit(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `idlink` (`qid` CHAR(12) NOT NULL,`steamId` CHAR(17) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        self.connection.commit()

    def executeWithReturn(self,command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def executeWithCommit(self,command):
        self.cursor.execute(command)
        self.connection.commit()

    def executeWithCount(self,command):
        return self.cursor.execute(command)