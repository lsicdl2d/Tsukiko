from sqlalchemy import create_engine

from .config import Config


class Database:
    def __init__(self):
        config = Config().config.database
        self.engine = create_engine(f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.name}")