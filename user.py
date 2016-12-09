import sqlite3
import hashlib

DATABASE = "data.db"

def add_user(username, password):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    c.execute(query, (username, hashlib.sha1(password).hexdigest()))
    db.commit()
    db.close()

def get_user(**kwargs):
    if not kwargs:
        return None

    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    criterion = []
    params = []
    for k,v in kwargs.items():
        criterion.append("%s = ?" % k)
        params.append(str(v))

    query = "SELECT * FROM users WHERE %s" % " AND ".join(criterion)
    c.execute(query, params)

    result = c.fetchone()
    db.close()
    return result

def get_UID(username):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("SELECT id FROM users WHERE username = '" + username + "'")
    return c.fetchone()[0]

def get_stories(uid):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "SELECT DISTINCT stories.storyid,stories.title from updates,stories WHERE userid = ? AND updates.storyid = stories.storyid"
    c.execute(query, (uid,))

    result = c.fetchall()
    db.close()
    return result if result else []

def get_info(uid):
    results = get_user(id=uid)
    info = {
        'uid' : results [0],
        'username' : results[1],
      
        }
    return info

#For now, only work with parameters path and uid
def add_pic(path,uid):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "INSERT INTO pics (path,userID) VALUES (?, ?)"
    c.execute(query,(path,uid))

    db.commit()
    db.close()
    
