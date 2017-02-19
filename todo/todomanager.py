import sqlite3

from todotypes import Todo

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
