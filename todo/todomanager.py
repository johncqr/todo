import argparse
import os
import sqlite3

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

from todotypes import Todo

# Google Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_creds():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'todo-googlesheetsapi.json')
    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run_flow(flow, store, flags)
    return credentials

TABLE_HEADERS = "Description TEXT, Completed VARCHAR(255), Created_On timestamp, Completed_On timestamp, Updated_On timestamp"
SS_FIELDS = ('Completed?', 'Description', 'Created on', 'Completed on', 'Updated on')

def todoify_db(row):
    ''' Returns Todo object using sqlite3 row information '''
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

    def edit(self, i, new_description):
        self.__storage[i].edit_desc(new_description)

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
        c.executemany('INSERT INTO todo VALUES (?,?,?,?,?)', (t.rowify_db() for t in self.__storage))
        conn.commit()
        conn.close()

    def from_db(self, db_file):
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM todo'):
            t = todoify_db(row)
            if t.is_complete():
                self.__count_completed += 1
            self.__count += 1
            self.__storage.append(t)

    def to_ss_new(self, ss_title):
        # Validate
        CREDS = get_creds()
        SHEETS = discovery.build('sheets', 'v4', http=CREDS.authorize(Http()))

        # Create new sheet
        data = {'properties': {'title': ss_title}}
        res = SHEETS.spreadsheets().create(body=data).execute()
        sheet_id = res['spreadsheetId']

        # Add data
        rows = [t.rowify_ss() for t in self.__storage]
        rows.insert(0, SS_FIELDS)
        data = {'values': rows}
        SHEETS.spreadsheets().values().update(spreadsheetId=sheet_id,
                                              range='A1', body=data,
                                              valueInputOption='USER_ENTERED').execute()

        # Formatting
        requests = []
        requests.append([{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "startRowIndex": 0,
                            "endRowIndex": self.__count+1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1,
                            }
                        ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_CONTAINS",
                            "values": [
                                {
                                    "userEnteredValue": "YES"
                                    }
                                ]
                            },
                        "format": {
                            "textFormat": {
                                "bold": True
                                },
                            "backgroundColor": { "green": 1 }
                            }
                        }
                    },
                "index": 0
                }
            },
            {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "startRowIndex": 0,
                            "endRowIndex": self.__count+1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1,
                            }
                        ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_CONTAINS",
                            "values": [
                                {
                                    "userEnteredValue": "NO"
                                    }
                                ]
                            },
                        "format": {
                            "textFormat": {
                                "bold": True
                                },
                            "backgroundColor": { "red": 1 }
                            }
                        }
                    },
                "index": 0
                }
            }])
        data = {"requests": requests}
        SHEETS.spreadsheets().batchUpdate(spreadsheetId=sheet_id,
                                              body=data).execute()

    def from_ss(self, sheet_id):
        return


        

