from datetime import datetime

class Todo:
    DATETIME_FORMAT = "%B %d, %Y %I:%M:%S %p"

    def __init__(self, description="", created_on=datetime.now(), completed_on=None, updated_on=None):
        '''Initializes a Todo object. Allows for created_on/completed_on/updated_on to be provided as a datetime or string (according to DATETIME_FORMAT).'''
        self.__desc = description
        if type(created_on) == str:
            created_on = datetime.strptime(created_on, Todo.DATETIME_FORMAT)
        self.__created_on = created_on
        if completed_on == 'N/A':
            completed_on = None
        elif type(completed_on) == str:
            completed_on = datetime.strptime(completed_on, Todo.DATETIME_FORMAT)
        self.__completed_on = completed_on
        self.__completed = completed_on != None
        if type(updated_on) == str:
            updated_on = datetime.strptime(updated_on, Todo.DATETIME_FORMAT)
        self.__updated_on = updated_on if updated_on else self.__created_on

    ## Public ##

    # Query todo
    def quick_view(self):
        return "[{}] {}".format('X' if self.__completed else ' ', self.__desc)

    def is_complete(self):
        return self.__completed

    def created_on(self):
        return self.__created_on.strftime(Todo.DATETIME_FORMAT)

    def completed_on(self):
        if self.__completed:
            return self.__completed_on.strftime(Todo.DATETIME_FORMAT)
        else:
            return 'N/A'

    def updated_on(self):
        return self.__updated_on.strftime(Todo.DATETIME_FORMAT)

    def rowify_db(self):
        '''Returns tuple containing Todo object information for insert into sqlite3 database.'''
        return (self.__desc, 'YES' if self.__completed else 'NO', self.__created_on, self.__completed_on, self.__updated_on)

    def rowify_ss(self):
        '''Returns tuple containing Todo object information for insert into Google spreadsheet.'''
        return ('YES' if self.__completed else 'NO', self.__desc, self.created_on(), self.completed_on(), self.updated_on())

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


    ## Private ##

    def __repr__(self):
        return "[{}] {} \n  Created on: {}\n  Completed on: {}\n  Last updated on: {}\n".format(
            'X' if self.__completed else ' ',
            self.__desc,
            self.created_on(),
            self.completed_on(),
            self.updated_on(),
            )
