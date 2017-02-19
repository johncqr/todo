from datetime import datetime
from pypz import timezone


class Todo:
    def __init__(self, description):
        self.__created_at = datetime.now()
        self.__desc = description
        self.__completed = False

