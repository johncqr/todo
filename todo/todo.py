import os

from todomanager import TodoManager

LONG_MENU = '''
Commands (case sensitve) and Usage:
    l       List all entries
    n       Create new entry
    c       Checkmark / complete ([X]) entry
    u       Uncheckmark / uncomplete ([ ]) entry
    d       Delete entry
    D       Delete all entries
    ED      Export all entries to sqlite3 database file
    EI      Import all entries from sqlite3 database file
    X       Close ToDo Manager
'''

# Prompts

def check_boundaries(i, b, e):
    return b <= i < e

def cancel_notification():
    print("Command cancelled.")

def error_notification():
    print("Please enter valid input.\n")

def confirmation_dialog(prompt):
    while True:
        confirm = input(prompt)
        if confirm == 'Y':
            return True
        elif confirm == 'n':
            return False
        error_notification()

def list_all(tm):
    if (tm.count() == 0):
        print("There are no entries to display.")
    else:
        for i, entry in enumerate(tm.all(), 1):
            print("{}: {}".format(i, entry))

def prompt_new(tm):
    desc = input("Description of new entry: ")
    tm.create(desc)

def prompt_complete(tm):
    if (tm.count() == 0):
        print("There are no entries to complete.")
        return
    while True:
        i = int(input("Index to complete: "))
        i -= 1
        if check_boundaries(i, 0, tm.count()):
            tm.complete(i)
            break
        else:
            error_notification()

def prompt_uncomplete(tm):
    if (tm.count() == 0):
        print("There are no entries to uncomplete.")
        return
    while True:
        i = int(input("Index to uncomplete: "))
        i -= 1
        if check_boundaries(i, 0, tm.count()):
            tm.uncomplete(i)
            break
        else:
            error_notification()

def prompt_delete(tm):
    if (tm.count() == 0):
        print("There are no entries to delete.")
        return
    while True:
        i = int(input("Index to delete: "))
        i -= 1
        if check_boundaries(i, 0, tm.count()):
            tm.delete(i)
            break
        else:
            error_notification()

def prompt_delete_all(tm):
    if (tm.count() == 0):
        print("There are no entries to delete.")
        return
    if confirmation_dialog("Confirm? (Y/n): "):
        tm.delete_all()
    else:
        cancel_notification()

def prompt_export_db(tm):
    if (tm.count() == 0):
        print("There are no entries to export.")
        return
    db_file = input("Enter database filename: ")
    if os.path.isfile(db_file):
        if confirmation_dialog("Confirm overwrite {}? (Y/n): ".format(db_file)):
            os.remove(db_file)
            tm.to_db(db_file)
            print("Database overwritten.")
        else:
            cancel_notification()
    else:
        if confirmation_dialog("Confirm creation of database {}? (Y/n): ".format(db_file)):
            tm.to_db(db_file)
            print("Database created.")
        else:
            cancel_notification()

def prompt_import_db(tm):
    db_file = input("Enter database filename: ")
    if os.path.isfile(db_file):
        if confirmation_dialog("Confirm import {}? (Y/n): ".format(db_file)):
            try:
                tm.from_db(db_file)
                print("Import succeeded.")
            except:
                Print("Import failed.")
        else:
            cancel_notification()
    else:
        print("Database does not exist. Import failed.")

def summary(tm):
    print("# of entries: {}\n# of completed entries: {}".format(tm.count(), tm.count_completed()))
    list_all(tm)

OPTIONS = {'l' : list_all,
           'n' : prompt_new,
           'c' : prompt_complete,
           'u' : prompt_uncomplete,
           'd' : prompt_delete,
           'D' : prompt_delete_all,
           'ED' : prompt_export_db,
           'ID' : prompt_import_db,
           }

def prompt(tm):
    while True:
        summary(tm)
        print(LONG_MENU)
        command = input("Enter command: ")
        if command == 'X':
            break
        elif command in OPTIONS:
            OPTIONS[command](tm)
            print()
        else:
            error_notification()

def main():
    tm = TodoManager()
    prompt(tm)
    
if __name__ == "__main__":
    main()