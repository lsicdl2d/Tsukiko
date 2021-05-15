from config.bot_config import mysql_rank_table
from .user import User


class Rank(User):
    def getUserRankInfo(self, steamid: str) -> dict:
        return self.executeWithReturn(f"SELECT * FROM {mysql_rank_table} WHERE steamId={steamid}")[0]
