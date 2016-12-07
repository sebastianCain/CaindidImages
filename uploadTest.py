import os
from flask import Flask, request, redirect, url_for#, send_from_directory <-- Unnecessary?
from werkzeug.utils import secure_filename


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
        '''#check if there is actually file uploaded by user
        if 'file' not in request.files:
            flash("No file")
            return redirect(request.url)

        ^the lines of code below already cover this'''
        
        file = request.files['file']

        #check if filename is empty
        '''if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        ^I lied, i think browsers do this for us, we dont really need it'''
        
        #if file is uploaded and filename is valid, save to the specified path (directory)
        if file and checkFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(path,filename))
            return "Image uploaded."
    return '''
    <!DOCTYPE html>
    <title>Upload New File</title>
    <form method='POST' action="" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

if __name__ == "__main__":
    app.debug = True
    app.run()
