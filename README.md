Caindid Images
==============
by Sea Bass Cain, Yuxuan Chen, Jiaqi Gao, Lawrence Liu
----------------------------------------------------------------------------
Caindid Images is a website where users can upload images (locally or with a url) and view the images other people have uploaded. Did you spot something cool and happened to take an impromptu, candid shot of it? Upload it immeadiately and the incorporated Google Maps will display where you were when you uploaded so friends, family, pets, and strangers can also go to that location and spot something cool themselves.

To use our website, first insert the Clarifai client_id and client_secret in app.py in lines 9 and 10. Then insert the Cloudinary secret key in utils.py line 11. Activate your virtual environment then simply run "python app.py" in your terminal and go to http://127.0.0.1:5000 in your browser. If you are not logged in, you may only browse the gallery of uploaded images. However, once registered, you may log in and upload your own images, whether locally from your machine or from a url. Only proper image files will be accepted. You may also see where users uploaded their images. Upon clicking an image, tags below the image can be viewed. Once registered, you gain access to your profile, where you can see all your uploaded images.
