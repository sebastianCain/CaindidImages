import urllib, urllib2, json, base64, time, hashlib, StringIO

def getTags(url, accesstoken):
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url="+url+"&access_token="+accesstoken)
    response = u.read()
    data = json.loads(response)
    return data["results"][0]["result"]["tag"]["classes"]

def uploadPic (path):
    
    CLOUDINARY_SECRET = "85ML_d2dPhlbbCTJ0h-HXL4UvZQ"
    
    #encode image
    with open(path, "rb") as image:
        encoded_image = base64.b64encode(image.read())
    utime = int(time.time())
    encoder = hashlib.sha1()
    encoder.update("timestamp=" + str(utime) + CLOUDINARY_SECRET)
    datadict = {"file": "data:image/jpg;base64," + encoded_image,
                "api_key": "246477329826533",
                "timestamp": str(utime),
                "signature": encoder.hexdigest()
                }
    encodeddata = urllib.urlencode(datadict)
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib2.Request("https://api.cloudinary.com/v1_1/dv5y12rxk/image/upload", encodeddata, headers)
    
    try:
        u = urllib2.urlopen(req)
        response = u.read()
        data = json.loads(response)
    except urllib2.HTTPError as e:
        print("ERROR OUTPUT: " + e.read())
    return data["url"]

'''
in user.py

def add_tag(path):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    query = "INSERT INTO pics WHERE [path = path of image] [this tag]"
    c.execute(query)

    db.commit()
    db.close()
'''
