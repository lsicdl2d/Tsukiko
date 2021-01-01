from decimal import Decimal
from .user import User
from .exception import ItemNotFoundError, UserNotLoginError, VehicleNotFoundError
from config.bot_config import mysql_uconomy_table,mysql_uconomy_shop_item_table,mysql_uconomy_shop_vehicle_table

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

    def getShopVehicleInfo(self, vehicleid: str) -> dict:
        return self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehicle_table} WHERE id = '{vehicleid}';")[0]

    def searchShopItem(self, itemname: str) -> list:
        search_result = self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE itemname LIKE '%{itemname}%';")
        if bool(search_result):
            return search_result
        else:
            raise ItemNotFoundError

    def searchShopVehicle(self, vehiclename: str) -> list:
        search_result = self.executeWithReturn(f"SELECT * FROM {mysql_uconomy_shop_vehicle_table} WHERE vehiclename LIKE '%{vehiclename}%';")
        if bool(search_result) :
            return search_result
        else:
            raise VehicleNotFoundError

    def setShopItem(self, itemid: str, itemname: str, cost: str, buyback: str):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_item_table} SET itemname='{itemname}',cost='{cost}',buyback='{buyback}' WHERE id={itemid};")

    def setShopVehicle(self, vehicleid: str, vehiclename: str, cost: str, buyback: str):
        self.executeWithCommit(f"UPDATE {mysql_uconomy_shop_vehicle_table} SET itemname='{vehiclename}',cost='{cost}',buyback='{buyback}' WHERE id={vehicleid};")

