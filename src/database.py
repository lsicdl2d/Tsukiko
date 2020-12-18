import pymysql.cursors
import pymysql
from config.bot_config import *
from .exception import *

class database(object):
    def __init__(self):
        self.connection = pymysql.connect(host=mysql_host,user=mysql_user,password=mysql_password,db=mysql_db,charset=mysql_charset,cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def check_user(self,qid):
        if self.cursor.execute(f"SELECT * FROM idlink WHERE qid = '{qid}';") != 0:
            return True
        else:
            return False

    def check_user_login(self,steamid):
        if self.cursor.execute(f"SELECT * FROM {mysql_uconomy_table} WHERE steamId = '{steamid}';") != 0:
            return True
        else:
            return False

    def user_init(self, qid, steamid):
        if not self.check_user(qid):
            if self.check_user_login(steamid):
                self.cursor.execute(f"INSERT INTO idlink (qid,steamId) VALUE ('{qid}', '{steamid}');")
                self.connection.commit()
            else:
                raise UserNotLoginError
        else:
            raise UserAlreadyHaveError

    def database_init(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `idlink` (`qid` CHAR(12) NOT NULL,`steamId` CHAR(17) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        self.connection.commit()

    def get_steamId(self,qid):
        if self.check_user(qid):
            self.cursor.execute(f"SELECT * FROM idlink WHERE qid = '{qid}'")
            return self.cursor.fetchone().get('steamId')
        else:
            raise UserNotFoundError
