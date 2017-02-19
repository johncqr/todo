import sqlite3

from todotypes import Todo

TABLE_HEADERS = "Description TEXT, Completed VARCHAR(255), Created_On timestamp, Completed_On timestamp, Updated_On timestamp"

def todoify(row):
    return Todo(row[0], row[2], row[3], row[4])

class TodoManager:
    """Handles managing, importing, and exporting Todo objects."""
    def __init__(self):
        self.__storage = list()    # Todos are held in a list
        self.__count = 0   # Current number of Todos
        self.__count_completed = 0

    def create(self, description):
        self.__count += 1
        self.__storage.append(Todo(description))

    def delete(self, i):
        self.__count -= 1
        if self.__storage[i].is_complete():
            self.__count_completed -= 1
        return self.__storage.pop()

    def complete(self, i):
        self.__count_completed += 1
        self.__storage[i].complete()

    def uncomplete(self, i):
        self.__count_completed -= 1
        self.__storage[i].uncomplete()

    def delete_all(self):
        self.__count = 0
        self.__count_completed = 0
        self.__storage.clear()

    def all(self):
        return self.__storage

    def count(self):
        return self.__count

    def count_completed(self):
        return self.__count_completed

    def to_db(self, db_file):
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('CREATE TABLE todo ({})'.format(TABLE_HEADERS))
        c.executemany('INSERT INTO todo VALUES (?,?,?,?,?)', (t.rowify() for t in self.__storage))
        conn.commit()
        conn.close()

    def from_db(self, db_file):
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM todo'):
            t = todoify(row)
            if t.is_complete():
                self.__count_completed += 1
            self.__count += 1
            self.__storage.append(t)

