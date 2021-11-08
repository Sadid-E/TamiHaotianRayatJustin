import sqlite3   #enable control of an sqlite database

DB_FILE='database.db'
db = sqlite3.connect(DB_FILE, check_same_thread=False)


def create_tables():
    c = db.cursor()
    command = 'CREATE TABLE IF NOT EXISTS entries (entry_id INTEGER PRIMARY KEY, title TEXT, entry_text TEXT, user_id INTEGER)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)    # run SQL statement

    command = 'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)

    db.commit() #save changes

def create_user(username, password):
    c = db.cursor()
    c.execute(f'INSERT INTO users (username, password) VALUES (?, ?);', (username, password))
    db.commit()

def add_entry(title, entry_text, user_id):
    c = db.cursor()
    c.execute(f'INSERT INTO entries (title, entry_text, user_id) VALUES (?, ?, ?)', (title, entry_text, user_id))
    db.commit() #save changes

def edit_entry(entry_id, entry_text, title):
    c = db.cursor()
    c.execute(f'UPDATE entries SET entry_text = ?, title = ? where entry_id == ?', (entry_text, title, entry_id))
    db.commit()

def delete_entry(entry_id):
    c = db.cursor()
    c.execute(f'delete from entries where entry_id == ?', (entry_id, ))
    db.commit()

def get_entry(entry_id):
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where entry_id == ?', (entry_id, )))
    if(len(result) == 0):
        return None
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result][0]

def get_entries_of_user(user_id, offset, limit):
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where user_id == ? order by entry_id limit ? offset ? ', (user_id, limit, offset)))
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result]
def authenticate(username, password):
    c = db.cursor()
    result = list(c.execute(f'SELECT user_id from users where username == ? and password == ?', (username, password)))
    if(len(result) == 0): #length 0 means that password/username combination had no match
        return None
    return result[0][0] #user_id

def get_username_from_id(user_id):
    c = db.cursor()
    result = list(c.execute(f'SELECT username from users where user_id == ?', (user_id, )))[0][0]
    print(result)
    return result

def getMostRecentEntry(user_id):
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where user_id == ? order by entry_id DESC limit 1', (user_id, )))
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result][0]

def printEverything():
    print(list(db.cursor().execute("select * from entries")))
