#Adding all the potentially useful clarifai tag request stuffs

'''curl "https://api.clarifai.com/v1/tag/?url=https://samples.clarifai.com/metro-north.jpg"
  -H "Authorization: Bearer {UjnFoZqHIByaxZDPdXI1yCrnIZG0Nd}"


curl "https://api.clarifai.com/v1/tag/" \
  -X POST -F "encoded_data=@/Users/USER/my_image.jpeg" \
  -H "Authorization: Bearer {UjnFoZqHIByaxZDPdXI1yCrnIZG0Nd}"'''

from flask import Flask, render_template
import urllib2, json

app = Flask(__name__)

@app.route("/")
def root():
    u = urllib2.urlopen("https://api.clarifai.com/v1/tag?url=https://samples.clarifai.com/metro-north.jpg&access_token=Yb7j7UYe047dQPrWgygvovE2D2qKv6")
    response = u.read()
    data = json.loads( response )
    return render_template("test.html", stuff = data["results"][0]["result"]["tag"]["classes"])


if __name__ == "__main__":
    app.debug = True
    app.run()


#output stored in 'results' key as an array
#response[results[tag[classes]]]
