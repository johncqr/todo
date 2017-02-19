import sqlite3

from todotypes import Todo

class TodoManager:
    """Handles managing, importing, and exporting Todo objects."""
    def __init__(self):
        STORAGE = list()    # Todos are held in a list
        N = 0   # Current number of Todos

    def create(description):
        COUNT += 1
        STORAGE.append(Todo(description))

    def delete(i):
        COUNT -= 1
        return STORAGE.pop()

    def delete_all():
        STORAGE.clear()

    def all():
        return STORAGE

    def count():
        return N

