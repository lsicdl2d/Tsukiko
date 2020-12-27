from decimal import Decimal
from .user import User
from .exception import UserNotLoginError
from config.bot_config import mysql_uconomy_table,mysql_uconomy_shop_item_table,mysql_uconomy_shop_vehice_table

class Uconomy(User):
    def getUserBalance(self,steamid):
        if self.checkUserLogin(steamid):
            return self.executeWithReturn(f"SELECT balance FROM {mysql_uconomy_table} WHERE steamId = {steamid};")[0]['balance']
        else:
            raise UserNotLoginError

    def setUserBalance(self, steamid, balance):
        '''
        传入的balance参数需为Decimal
        '''
        if self.checkUserLogin(steamid):
            self.executeWithCommit(f"UPDATE {mysql_uconomy_table} SET balance = {Decimal.to_eng_string(balance)} WHERE steamId = '{steamid}';")
        else:
            raise UserNotLoginError

class Shop(User):
    def getShopItemInfo(self, itemid):
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE id = '{itemid}';")[0]

    def getShopVehiceInfo(self, vehiceid):
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE id = '{vehiceid}';")[0]

    def searchShopItem(self, itemname):
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE itemname LIKE '%{itemname}%';")

    def searchShopVehice(self, vehicename):
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE vehiclename LIKE '%{vehicename}%';")

    def setShopItem(self, itemid, itemname, cost, buyback):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_item_table} SET itemname='{itemname}',cost='{cost}',buyback='{buyback}' WHERE id={itemid};")

    def setShopVehice(self, vehiceid, vehicename, cost, buyback):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_vehice_table} SET itemname='{vehicename}',cost='{cost}',buyback='{buyback}' WHERE id={vehiceid};")

