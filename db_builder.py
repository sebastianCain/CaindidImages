import sqlite3

DATABASE = "data.db"

def create_tables():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS pics (link TEXT, userID INTEGER, tags TEXT, upvotes INTEGER")
    #not sure if the categories are aight here
    db.commit()
    db.close()
