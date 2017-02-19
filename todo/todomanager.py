import sqlite3

from todotypes import Todo

class TodoManager:
    """Handles managing, importing, and exporting Todo objects."""
    def __init__(self):
        self.STORAGE = list()    # Todos are held in a list
        self.COUNT = 0   # Current number of Todos

    def create(self, description):
        self.COUNT += 1
        self.STORAGE.append(Todo(description))

    def delete(self, i):
        self.COUNT -= 1
        return self.STORAGE.pop()

    def delete_all(self):
        self.STORAGE.clear()

    def all(self):
        return self.STORAGE

    def count(self):
        return self.COUNT
