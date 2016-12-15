import sqlite3
import os

DATABASE = "data.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS pics (path TEXT, userID INTEGER, name TEXT, tags TEXT, lat TEXT, lon TEXT)")
    
    db.commit()
    db.close()
