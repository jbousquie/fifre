# Classe statique Tools
from datetime import datetime
import uuid


class Tools:
    # returns a date as a string
    @staticmethod
    def stringNow() -> str:
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H:%M:%S')
        return strnow

    # generates an unique random string
    @staticmethod
    def generate_unique_id() -> str:
        id: str = str(uuid.uuid4())
        return id


