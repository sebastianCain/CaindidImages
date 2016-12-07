import os
from flask import Flask, request, redirect, url_for#, send_from_directory <-- Unnecessary?
from werkzeug.utils import secure_filename
import urllib.request

app = Flask(__name__)
path="data"
#app.config['UPLOAD_FOLDER'] = "data"
#Pretty sure we dont need this fancy config stuff^^^
extensions = set(['png','jpg','jpeg'])


#check if the filename is an image
def checkFile(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in extensions

# if methods = 'GET' generate html page where user can upload picture
# if methods = 'POST' save file to /data
@app.route("/", methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == "":
            print "LINK"
            print request.form['link']
            urlretrieve(request.form['link'],"test.jpg")
    #if file is uploaded and filename is valid, save to the specified path (directory)
        elif file and checkFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(path,filename))
            return "Image uploaded."
    return '''
<!DOCTYPE html>
<title>Upload New File</title>
<form method='POST' action="" enctype="multipart/form-data">
<input type="file" name="file">
<input type="text" name="link">
<input type="submit" value="Upload">
</form>
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
