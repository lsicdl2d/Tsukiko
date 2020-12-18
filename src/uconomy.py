from config.bot_config import *
import pymysql.cursors
from decimal import Decimal
from .database import database,UserNotLoginError

class uconomy(database):
    def get_user_balance(self,steamid):
        if self.check_user_login(steamid):
            self.cursor.execute(f"SELECT * FROM {mysql_uconomy_table} WHERE steamId = {steamid}")
            return self.cursor.fetchone().get('balance')
        else:
            raise UserNotLoginError

    def set_user_uconomy(self, steamid, balance):
        if self.check_user_login(steamid):
            self.cursor.execute(f"UPDATE {mysql_uconomy_table} SET balance = {Decimal.to_eng_string(balance)} WHERE steamId = '{steamid}';")
            self.connection.commit()
        else:
            raise UserNotLoginError

class shop(database):
    def get_shop_item_info(self, itemid):
        self.cursor.execute(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE id = '{itemid}'")
        return self.cursor.fetchone()

    def get_shop_vehice_info(self, vehiceid):
        self.cursor.execute(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE id = '{vehiceid}'")
        return self.cursor.fetchone()

    def search_shop_item(self, itemname):
        self.cursor.execute(f"SELECT * FROM {mysql_uconomy_shop_item_table} WHERE itemname LIKE '%{itemname}%';")
        return self.cursor.fetchall()

    def search_shop_vehice(self, vehicename):
        self.cursor.execute(f"SELECT * FROM {mysql_uconomy_shop_vehice_table} WHERE vehiclename LIKE '%{vehicename}%';")
        return self.cursor.fetchall()

    def set_shop_item(self, itemid, itemname, cost, buyback):
        self.cursor.execute(f"UPDATE {mysql_uconomy_shop_item_table} SET itemname='{itemname}',cost='{cost}',buyback='{buyback}' WHERE id={itemid};")
        self.connection.commit()

    def set_shop_vehice(self, vehiceid, vehicename, cost, buyback):
        self.cursor.execute(f"UPDATE {mysql_uconomy_shop_vehice_table} SET itemname='{vehicename}',cost='{cost}',buyback='{buyback}' WHERE id={vehiceid};")
        self.connection.commit()

