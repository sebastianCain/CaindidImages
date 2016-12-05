import flickr_api
import urllib

flickr_api.set_keys(api_key = "422c82e0e5e7b17dd63a6de838ae771b", api_secret = "ad5635f246c0274a")


user = flickr_api.Person.findByUserName("OOYUKIOO")
photos = user.getPublicPhotos()
print photos.info.total
