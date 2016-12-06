import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

folderPath = "/data"
extensions = set(['png','jpg','jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = folderPath

#check if the filename is valid
def checkFile(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in extensions

# if methods = 'GET' generate html page where user can upload picture
# if methods = 'POST' save file to /data
@app.route("/", methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #check if there is actually file uploaded by user
        if 'file' not in request.files:
            flash("No file")
            return redirect(request.url)
        
        file = request.files['file']
        #check if filename is empty
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        #if file is uploaded and filename is valid, save to /data directory
        #>>>!!! BUG !!!<<<
        #ERROR MESSAGE :IOError: [Errno 13] Permission denied
        if file and checkFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return "Done"
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
