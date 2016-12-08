import sqlite3
import os

DATABASE = "data.db"

def create_tables(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS pics (path TEXT, userID INTEGER, tags TEXT, upvotes INTEGER)")
    #not sure if the categories are aight here
    pics = os.listdir(path)
    print pics
    
    db.commit()
    db.close()
