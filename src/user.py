import pymysql.cursors
import pymysql
from config.bot_config import mysql_uconomy_table
from .exception import UserAlreadyHaveError,UserNotLoginError,UserNotFoundError
from .database import Database

class User(Database):
    def checkUser(self,qid: str):
        if self.executeWithCount(f"SELECT * FROM userinfo WHERE qid = '{qid}';") != 0:
            return True
        else:
            return False

    def userDatabaseInit(self):
        self.executeWithCommit("CREATE TABLE IF NOT EXISTS `userinfo` (`qid` CHAR(12) NOT NULL,`steamId` CHAR(17) NOT NULL,`permission` TINYINT NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    def checkUserLogin(self,steamid: str):
        if self.executeWithCount(f"SELECT * FROM {mysql_uconomy_table} WHERE steamId = '{steamid}';") != 0:
            return True
        else:
            return False

    def userInit(self, qid: str, steamid: str):
        if not self.checkUser(qid):
            if self.checkUserLogin(steamid):
                self.executeWithCommit(f"INSERT INTO userinfo (qid,steamId,permission) VALUE ('{qid}', '{steamid}', 0);")
            else:
                raise UserNotLoginError
        else:
            raise UserAlreadyHaveError

    def getSteamId(self,qid: str):
        if self.checkUser(qid):
            return self.executeWithReturn(f"SELECT steamId FROM userinfo WHERE qid = '{qid}'")[0]['steamId']
        else:
            raise UserNotFoundError
