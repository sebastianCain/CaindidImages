import urllib, urllib2, json, base64, time, hashlib, StringIO

def getTags(url, accesstoken):
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url=/"+url+"&access_token="+accesstoken)
    response = u.read()
    data = json.loads(response)
    return data["results"][0]["result"]["tag"]["classes"]

def uploadPic (path):
    #encode image
    with open(path, "rb") as image:
        #encoded_image = bytearray(image.read())
        #imagestr = StringIO.StringIO(encoded_image)
        #imagestr.name = "file"
        encoded_image = base64.b64encode(image.read())
    #paramdict = {'quality':'2','category':'1','debug':'0', 'image': encoded_image}
    #params = urllib.urlencode(paramdict)
    
    #encode auth header
    #authstr = "Basic " + base64.b64encode("api:" + "N5bZsPRvTbuuTmdrXykaLC7WJPmnrW3N")
        
    #create request
    #req = urllib2.Request("https://api.cloudinary.com/v1_1/dv5y12rxk/image/upload")
    #print("START PARAMS\n" + params + "\nEND PARAMS")
    #add headers
    #req.add_header("Authorization", authstr)
    utime = int(time.time())
    encoder = hashlib.sha1()
    encoder.update("timestamp=" + str(utime) + "85ML_d2dPhlbbCTJ0h-HXL4UvZQ")
    datadict = {"file": "data:image/jpg;base64," + encoded_image,
                "api_key": "246477329826533",
                "timestamp": str(utime),
                "signature": encoder.hexdigest()
                }
    encodeddata = urllib.urlencode(datadict)
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib2.Request("https://api.cloudinary.com/v1_1/dv5y12rxk/image/upload", encodeddata, headers)
    
    print("REQ DATA\n" + req.data)
    print("REQ HEADERS\n" + urllib.urlencode(req.headers))
    print
    try:
        u = urllib2.urlopen(req)
        response = u.read()
        data = json.loads(response)
        print(data)
    except urllib2.HTTPError as e:
        print("ERROR OUTPUT: " + e.read())
    
    #return data
    #except urllib2.HTTPError as e:
        #print(e.read() + "AHHAAHAHAH")

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
