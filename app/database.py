import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


DB_FILE='database.db'

db = sqlite3.connect(DB_FILE)
c = db.cursor()

def create_tables():
    command = 'CREATE TABLE entries (id INTEGER PRIMARY KEY, title TEXT, user_id INTEGER KEY)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)    # run SQL statement

    command = 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, entry_ids TEXT)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

def write_entry_to_db(title, entry_text, entry_id, user_id):
    id = entry_id
    if entry_id == -1:
        command = 'SELECT id FROM entries ORDERBY ROWID DESC LIMIT 1'
        c.execute()

        id = c.fetchall()
        print(id)

    # file = open(f'{id}.txt', 'w')
    # file.write(entry_text)
    # file.close()
    #
    # command = f'INSERT INTO entries VALUES (0, \"{title}\", {user_id})'
