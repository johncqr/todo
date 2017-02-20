import os
import webbrowser

from todomanager import TodoManager, get_url

INTRO = '''
---------------------------
| Todo Manager by johncqr |
---------------------------
'''

LONG_MENU = '''
Commands (case sensitve) and Usage:
    l       List all entries with detailed information
    n       Create new entry
    c       Checkmark / complete ([X]) entry
    u       Uncheckmark / uncomplete ([ ]) entry
    e       Edit entry description
    d       Delete entry
    D       Delete all entries
    ED      Export all entries to sqlite3 database file
    ID      Import all entries from sqlite3 database file
    ES      Export all entries to Google Spreadsheet
    IS      Import all entries from Google Spreadsheet
    OS      Open known Google Spreadsheet in browser
    X       Close ToDo Manager
'''
SAVED_SHEETS_FILE = 'todo_sheets.txt'

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
            print("{}: {}".format(i, entry.quick_view()))

def list_all_verbose(tm):
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

def prompt_edit(tm):
    if (tm.count() == 0):
        print("There are no entries to edit.")
        return
    while True:
        i = int(input("Index to edit: "))
        i -= 1
        if check_boundaries(i, 0, tm.count()):
            new_desc = input("New description: ")
            tm.edit(i, new_desc)
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

def prompt_open_ss(tm):
    if not os.path.isfile(SAVED_SHEETS_FILE):
        print(SAVED_SHEETS_FILE + " does not exist. No known sheets to open.")
        return

    infile = open(SAVED_SHEETS_FILE, 'r')
    sheets = [e.split('|||') for e in infile.readlines()]
    infile.close()
    print("Known sheets (INDEX:  TITLE -> ID):")
    for i,entry in enumerate(sheets):
        print('{}:  {} -> {}'.format(i+1, entry[1].strip(), entry[0]))
    while True:
        i = int(input("Index to open: "))
        i -= 1
        if check_boundaries(i, 0, len(sheets)):
            break
        else:
            error_notification()
    webbrowser.open(get_url(sheets[i][0]))


def prompt_export_ss(tm):
    ss_title = input("Enter title of spreadsheet: ")
    print("Exporting...")
    url = tm.to_ss_new(ss_title)
    print("Export successful.")
    if confirmation_dialog("Open default browser to exported sheet? (Y/n): "):
        webbrowser.open(url)

def prompt_import_ss(tm):
    if not os.path.isfile(SAVED_SHEETS_FILE):
        print(SAVED_SHEETS_FILE + " does not exist. No known sheets to import.")
        return

    infile = open(SAVED_SHEETS_FILE, 'r')
    sheets = [e.split('|||') for e in infile.readlines()]
    infile.close()
    print("Known sheets (INDEX:  TITLE -> ID):")
    for i,entry in enumerate(sheets):
        print('{}:  {} -> {}'.format(i+1, entry[1].strip(), entry[0]))
    while True:
        i = int(input("Index to import: "))
        i -= 1
        if check_boundaries(i, 0, len(sheets)):
            break
        else:
            error_notification()
    print("Importing...")
    tm.from_ss(sheets[i][0])
    print("Import successful.")
   
def summary(tm):
    print("# of entries: {}\n# of completed entries: {}".format(tm.count(), tm.count_completed()))
    

OPTIONS = {
           'l' : list_all_verbose,
           'n' : prompt_new,
           'c' : prompt_complete,
           'u' : prompt_uncomplete,
           'e' : prompt_edit,
           'd' : prompt_delete,
           'D' : prompt_delete_all,
           'ED' : prompt_export_db,
           'ID' : prompt_import_db,
           'ES' : prompt_export_ss,
           'IS' : prompt_import_ss,
           'OS' : prompt_open_ss,
           }

def prompt(tm):
    while True:
        list_all(tm)
        command = input("\nEnter command ('h' for help): ")
        if command == 'X':
            print('Goodbye.')
            break
        elif command == 'h':
            print(LONG_MENU)
            summary(tm)
        elif command in OPTIONS:
            OPTIONS[command](tm)
            print()
        else:
            error_notification()

def main():
    tm = TodoManager()
    print(INTRO)
    prompt(tm)
    
if __name__ == "__main__":
    main()