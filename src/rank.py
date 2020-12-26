from .user import User
from config.bot_config import mysql_rank_table

class Rank(User):
    def getUserRankInfo(self, steamid):
        '''
        返回：{'steamId':xxx,'points':xxx,'lastDisplayName':xxx,'lastUpdated':xxx}
        '''
        return self.executeWithReturn(f"SELECT * FROM {mysql_rank_table} WHERE steamId={steamid}")[0]

