import pymysql.cursors
import pymysql
from config.bot_config import mysql_uconomy_table
from .exception import UserAlreadyHaveError,UserNotLoginError,UserNotFoundError
from .database import Database

class User(Database):
    def checkUser(self,qid):
        if self.executeWithCount(f"SELECT * FROM idlink WHERE qid = '{qid}';") != 0:
            return True
        else:
            return False

    def checkUserLogin(self,steamid):
        if self.executeWithCount(f"SELECT * FROM {mysql_uconomy_table} WHERE steamId = '{steamid}';") != 0:
            return True
        else:
            return False

    def userInit(self, qid, steamid):
        if not self.checkUser(qid):
            if self.checkUserLogin(steamid):
                self.executeWithCommit(f"INSERT INTO idlink (qid,steamId) VALUE ('{qid}', '{steamid}');")
            else:
                raise UserNotLoginError
        else:
            raise UserAlreadyHaveError

    def getSteamId(self,qid):
        if self.checkUser(qid):
            return self.executeWithReturn(f"SELECT steamId FROM idlink WHERE qid = '{qid}'")[0]
        else:
            raise UserNotFoundError
