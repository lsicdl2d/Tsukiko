from .database import database
from config.bot_config import mysql_rank_table

class rank(database):
    def get_user_rank_info(self, steamid):
        '''
        返回：{'steamId':xxx,'points':xxx,'lastDisplayName':xxx,'lastUpdated':xxx}
        '''
        self.cursor.execute(f"SELECT * FROM {mysql_rank_table} WHERE steamId={steamid}")
        return self.cursor.fetchone()
