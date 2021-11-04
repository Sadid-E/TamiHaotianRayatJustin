import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE='database.db'

def create_tables():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = 'CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, title TEXT, user_id INTEGER KEY)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)    # run SQL statement

    command = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

def write_entry_to_db(title, entry_text, entry_id, user_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id = entry_id
    if entry_id == -1:
        command = 'SELECT id FROM entries ORDER BY id DESC LIMIT 1'
        c.execute(command)

        ids = c.fetchall()
        if len(ids) == 0:
            id = 0
        else:
            id = ids[0][0] + 1

    file = open(f'{id}.txt', 'w')
    file.write(entry_text)
    file.close()

    command = f'INSERT INTO entries VALUES ({id}, "{title}", {user_id});'
    c.execute(command)

    db.commit() #save changes
    db.close()

def create_user(name, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = 'SELECT id FROM users ORDER BY id DESC LIMIT 1'
    c.execute(command)

    id = 0
    ids = c.fetchall()
    if len(ids) > 0:
        print(ids)
        id = ids[0][0] + 1
    print(id)

    command = f'INSERT INTO users VALUES ({id}, "{name}", "{password}");'
    c.execute(command)

    db.commit() #save changes
    db.close()
