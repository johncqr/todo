import sqlite3

import todotypes

class TodoManager:
    """Handles interfacing with the sqlite3 database (creating, deleting, querying todo entries)"""

    def connect(db_path):
        self.__conn = sqlite3.connect(db_path)
        self.__c = self.__conn.cursor()

    def disconnect():
        self.__conn.close()



