from python_json_config import ConfigBuilder


class Config:
    def __init__(self):
        builder = ConfigBuilder()
        self.config = builder.parse_config("config.json")
