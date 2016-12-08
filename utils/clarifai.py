from clarifai import rest
from clarifai.rest import ClarifaiApp
#import tinify
from clarifai.rest import Image as ClImage

CLARIFAI_APP_ID = "Y8pZV9ZL3UxoCsTzeg-lK4zz6nJDJmZ0bt0xheJA"
CLARIFAI_APP_SECRET = "RtqGr7kvfCdiyzCRZsJ2ElqdsjJpreydSkTCZUO4"

app = ClarifaiApp()

#to make a request:
def requestTags(imageName):
    model = app.models.get('general-v1.3')
    image = ClImage(url='/images/' + imageName)
    model.predict([image])

    #request response:
    dict = response["output"][0]["data"]["concepts"]
    keywords = []
    for i in dict:
        keywords.append(i["name"])
        #i["value"] is the likelihood of the tag relating to the image
    return keywords[:10]



print requestTags("train.png")

#tinify.key = "N5bZsPRvTbuuTmdrXykaLC7WJPmnrW3N
