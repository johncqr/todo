from datetime import datetime
import pytz


class Todo:
    DATETIME_FORMAT = '%B %d, %Y %I:%M:%S %p'

    def __init__(self, description="", created_on=datetime.now(), completed_on=None):
        self.__desc = description
        self.__created_on = created_on
        self.__completed_on = completed_on
        self.__completed = completed_on != None
        self.__updated_on = created_on

    # Query todo
    def view_desc(self):
        return self.__desc

    def is_complete(self):
        return self.__completed

    def created_on(self):
        return self.__created_on.strftime(Todo.DATETIME_FORMAT)

    def completed_on(self):
        if self.__completed:
            return self.__completed_on.strftime(Todo.DATETIME_FORMAT)
        else:
            return 'N/A'


    # Edit todo
    def complete(self):
        if not self.__completed:
            self.__completed_on = datetime.now()
            self.__completed = True

    def uncomplete(self):
        self.__completed_on = None
        self.__completed = False

    def edit_desc(self, new_desc):
        self.__updated_on = datetime.now()
        self.__desc = new_desc


    # Private

    def __repr__(self):
        return '[{}] {} \n  Created on: {}\n  Completed on: {}'.format(
            'X' if self.__completed else ' ',
            self.__desc,
            self.created_on(),
            self.completed_on(),
            )