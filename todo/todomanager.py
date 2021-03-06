import argparse
import os
import sqlite3

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

from todotypes import Todo

# Google Sheets API Globals
SCOPES = "https://www.googleapis.com/auth/spreadsheets"
CLIENT_SECRET_FILE = 'client_secret.json'
URL = "https://docs.google.com/spreadsheets/d/"

def get_creds():
    '''Obtains credentials to be used for Google Sheets API.'''
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
    '''Returns Todo object using sqlite3 row information.'''
    return Todo(row[0], row[2], row[3], row[4])

def todoify_ss(row):
    '''Returns Todo object using Google Sheet row information.'''
    return Todo(row[1], row[2], row[3], row[4])

def get_url(sheet_id):
    return URL+sheet_id

class TodoManager:
    '''Handles managing, importing, and exporting Todo objects.'''
    def __init__(self):
        self.__storage = list()    # Todos are held in a list
        self.__count = 0   # Current number of Todos
        self.__count_completed = 0  # Current number of completed Todos

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
        '''Exports storage to a sqlite3 db.'''
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('CREATE TABLE todo ({})'.format(TABLE_HEADERS))
        c.executemany('INSERT INTO todo VALUES (?,?,?,?,?)', (t.rowify_db() for t in self.__storage))
        conn.commit()
        conn.close()

    def from_db(self, db_file):
        '''Imports sqlite3 db to storage.'''
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM todo'):
            t = todoify_db(row)
            if t.is_complete():
                self.__count_completed += 1
            self.__count += 1
            self.__storage.append(t)

    def to_ss_new(self, ss_title):
        '''Exports storage to a new Google Spreadsheet.'''
        # Validate
        creds = get_creds()
        service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

        # Create new sheet
        data = {'properties': {'title': ss_title}}
        res = service.spreadsheets().create(body=data).execute()
        sheet_id = res['spreadsheetId']

        # Save id
        outfile = open('todo_sheets.txt', 'a')
        outfile.write('{}|||{}\n'.format(sheet_id, ss_title))
        outfile.close()

        # Add data
        rows = [t.rowify_ss() for t in self.__storage]
        rows.insert(0, SS_FIELDS)
        data = {'values': rows}
        service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                              range='A1', body=data,
                                              valueInputOption='USER_ENTERED').execute()

        # Formatting
        requests = []   # contains requests for API batchUpdate

        # Turn the background colors of "YES" cells to green and "NO" cells to red
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

        # send API request
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id,
                                              body=data).execute()
        return get_url(sheet_id)

    def from_ss(self, sheet_id):
        # Validate
        creds = get_creds()
        service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))

        # Get sheet
        range_name = 'A2:E'
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name).execute()

        # Store obtained rows in storage
        for row in result['values']:
            t = todoify_ss(row)
            if t.is_complete():
                self.__count_completed += 1
            self.__count += 1
            self.__storage.append(t)
