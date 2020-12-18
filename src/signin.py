from src.exception import UserAlreadySigninTodayError
import pymysql.cursors
import pymysql
from config.bot_config import *
import time
from decimal import Decimal
import random
from .uconomy import uconomy
from .database import database

uconomy = uconomy()

class signin(database):
    def signin_database_init(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `signin` (`qid` CHAR(12) NOT NULL,`timestamp` DECIMAL(38,6) NOT NULL,`continuedSignin` SMALLINT NOT NULL,`totalSignin` SMALLINT NOT NULL,`todaySignin` TINYINT NOT NULL,`lastReward` DECIMAL(38,2) NOT NULL, PRIMARY KEY ( `qid` )) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        self.connection.commit()

    def user_signin_init(self,qid):
        self.cursor.execute(f"INSERT INTO signin (qid, timestamp, continuedSignin, totalSignin, todaySignin, lastReward) VAlUES ({qid}, {time.time()},0,0,0,0)")

    def clear_today_signin(self):
        self.cursor.execute("UPDATE signin SET todaySignin=0")
        self.connection.commit()

    def check_today_signin(self,qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'")
        if self.cursor.fetchone().get('todaySignin') == 1:
            return True
        else:
            return False

    def check_user_signin(self,qid):
        if self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'") != 0:
            return True
        else:
            return False

    def check_continued_signin(self,qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'")
        time_difference = time.time() - self.cursor.fetchone().get('timestamp') 
        if time_difference < Decimal(172800):
            return True
        else:
            return False

    def get_continued_signin(self, qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'")
        return self.cursor.fetchone().get('continuedSignin')

    def get_total_signin(self, qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'")
        return self.cursor.fetchone().get('totalSignin')

    def get_last_signin_timestamp(self, qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid='{qid}'")
        return self.cursor.fetchone().get('timestamp')

    def add_total_signin(self,qid):
        '''
        +1
        '''
        self.cursor.execute(f"UPDATE signin SET totalSignin={self.get_total_signin(qid)+1}")
        self.connection.commit()

    def set_continued_signin(self,qid):
        '''
        自动检查是否连续签到
        '''
        if self.check_continued_signin(qid):
            self.cursor.execute(f"UPDATE signin SET continuedSignin={self.get_continued_signin(qid)+1}")
        else:
            self.cursor.execute(f"UPDATE signin SET continuedSignin=1")
        self.connection.commit()

    def set_last_reward(self,qid,reward):
        self.cursor.execute(f"UPDATE signin SET lastReward={reward} WHERE qid = '{qid}'")
        self.connection.commit()

    def set_signin_info(self,qid):
        self.cursor.execute(f"UPDATE signin SET timestamp={time.time()},todaySignin=1 WHERE qid = '{qid}'")
        self.connection.commit()

    def get_lastReward(self,qid):
        self.cursor.execute(f"SELECT * FROM signin WHERE qid = '{qid}'")
        return self.cursor.fetchone().get('lastReward')

    def signin(self,qid):
        if not self.check_user_signin(qid):
            self.user_signin_init(qid) #检测初次签到
        if not self.check_today_signin(qid):
            reward = random.randint(signin_min_get_balance,signin_max_get_balance) #获取基本奖励金
            uconomy.set_user_uconomy(self.get_steamId(qid),uconomy.get_user_balance(self.get_steamId(qid))+Decimal(reward)) #打钱
            if self.get_continued_signin(qid)%signin_continued_reward_day == 0 and self.get_continued_signin(qid) != 0: #连续签到x日特别打钱
                uconomy.set_user_uconomy(self.get_steamId(qid),uconomy.get_user_balance(self.get_steamId(qid))+Decimal(signin_continued_reward)) #打钱
                self.set_last_reward(qid,reward+signin_continued_reward) #记录上次打钱
            else:
                self.set_last_reward(qid,reward) #同上
            self.add_total_signin(qid)
            self.set_signin_info(qid)
        else:
            raise UserAlreadySigninTodayError
