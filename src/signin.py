from src.exception import UserAlreadySigninTodayError
import pymysql
from config.bot_config import signin_max_get_balance,signin_min_get_balance,signin_continued_reward,signin_continued_reward_day
import time
from decimal import Decimal
import random
from .uconomy import Uconomy
from .user import User

uconomy = Uconomy()

class Signin(User):
    def signinDatabaseInit(self):
        self.executeWithCommit("CREATE TABLE IF NOT EXISTS `signin` (`qid` CHAR(12) NOT NULL,`timestamp` DECIMAL(38,6) NOT NULL,`continuedSignin` SMALLINT NOT NULL,`totalSignin` SMALLINT NOT NULL,`todaySignin` TINYINT NOT NULL,`lastReward` DECIMAL(38,2) NOT NULL, PRIMARY KEY ( `qid` )) ENGINE=InnoDB DEFAULT CHARSET=utf8;")

    def userSigninInit(self,qid):
        self.executeWithCommit(f"INSERT INTO signin (qid, timestamp, continuedSignin, totalSignin, todaySignin, lastReward) VAlUES ({qid}, {time.time()},0,0,0,0);")

    def clearTodaySignin(self):
        self.executeWithCommit("UPDATE signin SET todaySignin=0")

    def checkTodaySignin(self,qid):
        if self.executeWithReturn(f"SELECT todaySignin FROM signin WHERE qid='{qid}';")[0]['todaySignin'] == 1:
            return True
        else:
            return False

    def checkUserSignin(self,qid):
        if self.executeWithCount(f"SELECT * FROM signin WHERE qid='{qid}';") != 0:
            return True
        else:
            return False

    def checkContinuedSignin(self,qid):
        time_difference = Decimal(time.time()) - self.getLastSigninTimestamp(qid)
        if time_difference < Decimal(172800):
            return True
        else:
            return False

    def getContinuedSignin(self, qid):
        return self.executeWithReturn(f"SELECT continuedSignin FROM signin WHERE qid='{qid}';")[0]['continuedSignin']

    def getTotalSignin(self, qid):
        return self.executeWithReturn(f"SELECT totalSignin FROM signin WHERE qid='{qid}';")[0]['totalSignin']

    def getLastSigninTimestamp(self, qid):
        return self.executeWithReturn(f"SELECT timestamp FROM signin WHERE qid='{qid}';")[0]['timestamp']

    def addTotalSignin(self,qid):
        '''
        +1
        '''
        self.executeWithCommit(f"UPDATE signin SET totalSignin={self.getTotalSignin(qid)+1} WHERE qid='{qid}'")

    def setContinuedSignin(self,qid):
        '''
        自动检查是否连续签到
        '''
        if self.checkContinuedSignin(qid):
            self.executeWithCommit(f"UPDATE signin SET continuedSignin={self.getContinuedSignin(qid)+1} WHERE qid='{qid}';")
        else:
            self.executeWithCommit(f"UPDATE signin SET continuedSignin=0 WHERE qid='{qid}';")

    def setLastReward(self,qid,reward):
        self.executeWithCommit(f"UPDATE signin SET lastReward={reward} WHERE qid='{qid}';")

    def setSigninInfo(self,qid):
        self.executeWithCommit(f"UPDATE signin SET timestamp={time.time()},todaySignin=1 WHERE qid='{qid}';")

    def getLastReward(self,qid):
        return self.executeWithReturn(f"SELECT lastReward FROM signin WHERE qid='{qid}';")[0]['lastReward']

    def signin(self,qid):
        if not self.checkUserSignin(qid):
            self.userSigninInit(qid) #检测初次签到
        if not self.checkTodaySignin(qid):
            reward = random.randint(signin_min_get_balance,signin_max_get_balance) #获取基本奖励金
            uconomy.setUserBalance(self.getSteamId(qid),uconomy.getUserBalance(self.getSteamId(qid))+Decimal(reward)) #打钱
            if self.getContinuedSignin(qid)%signin_continued_reward_day == 0 and self.getContinuedSignin(qid) != 0: #连续签到x日特别打钱
                uconomy.setUserBalance(self.getSteamId(qid),uconomy.getUserBalance(self.getSteamId(qid))+Decimal(signin_continued_reward)) #打钱
                self.setLastReward(qid,reward+signin_continued_reward) #记录上次打钱
            else:
                self.setLastReward(qid,reward) #同上
            self.addTotalSignin(qid)
            self.setSigninInfo(qid)
        else:
            raise UserAlreadySigninTodayError
