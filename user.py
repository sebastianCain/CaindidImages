import sqlite3
import hashlib
import re
import json
import urllib2
from urllib2 import urlopen

import socket
from freegeoip import get_geodata


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

def get_username(userID):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE id = '" + str(userID) + "'")
    return c.fetchone()[0]

def get_UID(username):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("SELECT id FROM users WHERE username = '" + username + "'")
    return c.fetchone()[0]

def match_UID(image):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute("SELECT userID FROM pics WHERE name = '" + image + "'")
    return c.fetchone()[0]


def get_info(uid):
    results = get_user(id=uid)
    info = {
        'uid' : results [0],
        'username' : results[1],
      
        }
    return info

api_key = "02faf2453733544398971093aec429153d210a5c1820321f93bfe6e6ed6fda23"
ip_address = urlopen('http://ip.42.pl/raw').read()

def getIPAddress(api_key,ip_address):
    api_endpoint = "http://api.ipinfodb.com/v3/ip-city/?key=" +api_key+"&ip="+ip_address+"&format=json"
    try:
        api_response = urllib2.urlopen(api_endpoint)
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON format error"
    
    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason

data = getIPAddress(api_key,ip_address)


#For now, only work with parameters path and uid
def add_pic(path,uid,name,tags):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    
    if data['statusCode'] == "OK":
        lat = data['latitude']
        lon = data['longitude']
        query = "INSERT INTO pics (path,userID,name,tags,lat,lon) VALUES (?, ?, ?, ?, ?,?)"
        c.execute(query,(path,uid,name,tags,lat,lon))
    else:
        query = "INSERT INTO pics (path,userID,name,tags) VALUES (?, ?, ?,?)"
        c.execute(query,(path,uid,name,tags))
        
    db.commit()
    db.close()

def get_pics(uid):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    if(uid=="all"):
        query = "SELECT path from pics"
        c.execute(query)
    else:
        query = "SELECT path FROM pics WHERE userID = ?"
        c.execute(query,(uid,))
    paths = c.fetchall()
    return paths

def get_name(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT name FROM pics WHERE path = ?"
    c.execute(query,(path,))
    n = c.fetchall()
    return n

def get_lat(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT lat FROM pics WHERE path = ?"
    c.execute(query,(path,))
    n = c.fetchall()
    return n

def get_lon(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT lon FROM pics WHERE path = ?"
    c.execute(query,(path,))
    n = c.fetchall()
    return n


def get_tags(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    query = "SELECT tags FROM pics WHERE path = ?"
    c.execute(query,(path,))
    p = c.fetchall()
    return p[0]
