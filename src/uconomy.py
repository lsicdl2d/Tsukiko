from decimal import Decimal
from .user import User
from .exception import ItemNotFoundError, UserNotLoginError, VehicleNotFoundError
from config.bot_config import mysql_uconomy_table,mysql_uconomy_shop_item_table,mysql_uconomy_shop_vehice_table

class Uconomy(User):
    def getUserBalance(self,steamid: str) -> Decimal:
        if self.checkUserLogin(steamid):
            return self.executeWithReturn(f"SELECT balance FROM {mysql_uconomy_table} WHERE steamId = {steamid};")[0]['balance']
        else:
            raise UserNotLoginError

    def setUserBalance(self, steamid: str, balance: Decimal):
        if self.checkUserLogin(steamid):
            self.executeWithCommit(f"UPDATE {mysql_uconomy_table} SET balance = {Decimal.to_eng_string(balance)} WHERE steamId = '{steamid}';")
        else:
            raise UserNotLoginError

class Shop(User):
    def getShopItemInfo(self, itemid: str) -> dict:
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE id = '{itemid}';")[0]

    def getShopVehiceInfo(self, vehiceid: str) -> dict:
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE id = '{vehiceid}';")[0]

    def searchShopItem(self, itemname: str) -> list:
        search_result = self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE itemname LIKE '%{itemname}%';")
        if bool(search_result):
            return search_result
        else:
            raise ItemNotFoundError

    def searchShopVehice(self, vehicename: str) -> list:
        search_result = self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE vehiclename LIKE '%{vehicename}%';")
        if bool(search_result) :
            return search_result
        else:
            raise VehicleNotFoundError

    def setShopItem(self, itemid: str, itemname: str, cost: str, buyback: str):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_item_table} SET itemname='{itemname}',cost='{cost}',buyback='{buyback}' WHERE id={itemid};")

    def setShopVehice(self, vehiceid: str, vehicename: str, cost: str, buyback: str):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_vehice_table} SET itemname='{vehicename}',cost='{cost}',buyback='{buyback}' WHERE id={vehiceid};")

