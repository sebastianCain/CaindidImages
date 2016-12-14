import urllib2, json

def getTags(url, accesstoken):
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url=/"+url+"&access_token="+accesstoken)
    response = u.read()
    data = json.loads(response)
    return data["results"][0]["result"]["tag"]["classes"]

def uploadPic (url, filename):
    req = urllib2.Request("https://api.tinify.com/shrink")
    data = {"user api": "N5bZsPRvTbuuTmdrXykaLC7WJPmnrW3N", "data-binary": filename, "dump-header": url}
    req.data = urllib.urlencode(data)
    u = urllib2.urlopen(req)
    response = u.read()
    data = json.loads(response)
    return data["location"]

'''
in user.py

def add_tag(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "INSERT INTO pics WHERE [path = path of image] [this tag]"
    c.execute(query)

    db.commit()
    db.close()



In app.py

import clarifai

#when you upload a picture
tags = clarifai.getTags(path+"/"+filename)
for tag in tags:
   add_tag(path+"/"+filename)


Then use html to display the tags
'''
