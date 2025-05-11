import os
from dotenv import load_dotenv

load_dotenv()  # Loads values from .env into os.environ

class Config:
    @staticmethod
    def get(key: str, default=None):
        return os.getenv(key, default)

    @staticmethod
    def get_bool(key: str, default=False):
        val = os.getenv(key)
        if val is None:
            return default
        return val.lower() in ["1", "true", "yes"]

    @staticmethod
    def get_int(key: str, default=0):
        try:
            return int(os.getenv(key, default))
        except ValueError:
            return default