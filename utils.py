import urllib, urllib2, json, base64

def getTags(url, accesstoken):
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url=/"+url+"&access_token="+accesstoken)
    response = u.read()
    data = json.loads(response)
    return data["results"][0]["result"]["tag"]["classes"]

def uploadPic (path):
    #encode image
    with open(path, "rb") as image:
        encoded_image = base64.b64encode(image.read())
    paramdict = {'quality':'2','category':'1','debug':'0', 'image': encoded_image}
    params = urllib.urlencode(paramdict)
    
    #encode auth header
    authstr = "Basic " + base64.b64encode("api:" + "N5bZsPRvTbuuTmdrXykaLC7WJPmnrW3N")

    #create request
    req = urllib2.Request("https://api.tinify.com/shrink", params)

    #add headers
    req.add_header("Authorization", authstr)
    req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-16")

    #perform request and retrieve data
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
