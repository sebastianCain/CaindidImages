import urllib2, json

#returns the url of the compressed image from tinypng
def uploadPic (url, filename):
    u = urllib2.urlopen("https://api.tinify.com/shrink?user_api:N5bZsPRvTbuuTmdrXykaLC7WJPmnrW3N&data-binary:@" + filename + "&dump-header:" + url)
    response = u.read()
    data = json.loads(response)
    return data["source"]["url"]
#Not sure that's the right link, refer to https://tinypng.com/developers/reference

'''
curl https://api.tinify.com/shrink \
     --user api:YOUR_API_KEY \
     --data-binary @unoptimized.jpg \
     --dump-header /dev/stdout
'''
