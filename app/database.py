import sqlite3   #enable control of an sqlite database
import random

DB_FILE='database.db'
db = sqlite3.connect(DB_FILE, check_same_thread=False)


def create_tables():
    """Creates the tables in the database to store entries and users"""
    c = db.cursor()
    command = 'CREATE TABLE IF NOT EXISTS entries (entry_id INTEGER PRIMARY KEY, title TEXT, entry_text TEXT, user_id INTEGER)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)    # run SQL statement

    command = 'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)'          # test SQL stmt in sqlite3 shell, save as string
    c.execute(command)

    db.commit() #save changes

def create_user(username, password):
    """Adds a user with a username and password into the users table of the database"""
    c = db.cursor()
    c.execute(f'INSERT INTO users (username, password) VALUES (?, ?);', (username, password)) 
    db.commit()

def add_entry(title, entry_text, user_id):
    """Adds an entry into the entries table, stores the text, title, and the user id of the associated account"""
    c = db.cursor()
    c.execute(f'INSERT INTO entries (title, entry_text, user_id) VALUES (?, ?, ?)', (title, entry_text, user_id))
    db.commit() 

def edit_entry(entry_id, entry_text, title):
    """Updates the text and title of an entry, entry id is not altered"""
    c = db.cursor()
    c.execute(f'UPDATE entries SET entry_text = ?, title = ? where entry_id == ?', (entry_text, title, entry_id))
    db.commit()

def delete_entry(entry_id):
    """Removes an entry from the table based on the entry id"""
    c = db.cursor()
    c.execute(f'delete from entries where entry_id == ?', (entry_id, ))
    db.commit()

def get_entry(entry_id):
    """Returns a list based on the entry id with values of the id, text, title, and assosciated user id"""
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where entry_id == ?', (entry_id, )))
    if(len(result) == 0): #if there is no entry with the id 
        return None
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result][0] #returning only the selected entry

def get_entries_of_user(user_id, offset, limit):
    """Returns a list of lists with user entries from the offset to the limit"""
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where user_id == ? order by entry_id limit ? offset ? ', (user_id, limit, offset)))
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result] #all the entries of a user
def authenticate(username, password):
    """Checks if the username and password match any login info in the users table"""
    c = db.cursor()
    result = list(c.execute(f'SELECT user_id from users where username == ? and password == ?', (username, password)))
    if(len(result) == 0): #length 0 means that password/username combination had no match
        return None
    return result[0][0] #user_id

def get_username_from_id(user_id):
    """returns the username given the user id"""
    c = db.cursor()
    result = list(c.execute(f'SELECT username from users where user_id == ?', (user_id, )))[0][0]
    return result

def getMostRecentEntry(user_id):
    """Returns the users most recent entry by ordering all of their entries in id order, with the entry of the largest id at the top"""
    c = db.cursor()
    result = list(c.execute(f'select entry_id, entry_text, title, user_id from entries where user_id == ? order by entry_id DESC limit 1', (user_id, )))
    return [{
        "entry_id": entry_id,
        "entry_text": entry_text,
        "title": title,
        "user_id": user_id
    } for (entry_id, entry_text, title, user_id) in result][0] #returning first entry in reordered list


def get_random_users():
    """Returns either 10 random users or all users to display as recommended blogs on the homepage"""
    c = db.cursor()
    rows = list(c.execute('SELECT COUNT(*) FROM users'))[0][0] #length of users table
    population_count = 10 if rows >= 10 else rows
    user_ids = random.sample(range(1,rows+1), population_count) #takes 10 distinct random users
    usernames = [get_username_from_id(user_id) for user_id in user_ids]
    return [
        {
            'username': username,
            'user_id': user_id
        } 
    for (username, user_id) in zip(usernames, user_ids)]
