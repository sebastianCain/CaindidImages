#Adding all the potentially useful clarifai tag request stuffs

curl "https://api.clarifai.com/v1/tag/?url=https://samples.clarifai.com/metro-north.jpg" \
  -H "Authorization: Bearer {access_token}"


curl "https://api.clarifai.com/v1/tag/" \
  -X POST -F "encoded_data=@/Users/USER/my_image.jpeg" \
  -H "Authorization: Bearer {access_token}"


#output stored in 'results' key as an array
#response[results[tag[classes]]]
