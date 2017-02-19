from todomanager import TodoManager

LONG_MENU = '''
Commands (case sensitve) and Usage:
    n       Create new entry
    d       Delete entry
    D       Delete all entries
    X       Close ToDo Manager
'''

# Prompts
def error_notification():
    print("Please enter valid input.\n")

def prompt_new(tm):
    desc = input("Description of new entry: ")
    tm.create(desc)

def prompt_delete(tm):
    if (tm.count() == 0):
        print("There are no entries to delete.")
        return

    while True:
        i = int(input("Index to delete: "))
        if (0 <= i-1 < tm.count()):
            tm.delete(i-1)
            break
        else:
            error_notification()

def prompt_delete_all(tm):
    while True:
        confirm = input("Confirm? (Y/n): ")
        if confirm == 'Y':
            tm.delete_all()
            break
        elif confirm == 'n':
            break
        error_notification()

def list_all(tm):
    print("# of entries: " + str(tm.count()))
    for i, entry in enumerate(tm.all(), 1):
        print("{}: {}".format(i, entry))

OPTIONS = {'n' : prompt_new,
           'd' : prompt_delete,
           'D' : prompt_delete_all,
           }

def prompt(tm):
    while True:
        list_all(tm)
        print(LONG_MENU)
        command = input("Enter command: ")
        
        if command == 'X':
            break

        if command in OPTIONS:
            OPTIONS[command](tm)
            print()
        else:
            error_notification()


def main():
    tm = TodoManager()
    prompt(tm)
    
if __name__ == "__main__":
    main()