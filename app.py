from flask import abort, Flask, render_template, request, redirect, url_for, session
import datetime, os
from werkzeug.utils import secure_filename

import hashlib
import db_builder
import user

#path for upload folder
path = "images"
app = Flask(__name__)

def validate_form(form, required_keys):
    """ Check if a dictionary contains all the required keys """
    return set(required_keys) <= set(form)

#login route
@app.route("/", methods=["POST", "GET"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html",username=session['username'])

#create a new account app route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # User has submitted a request to register an account
        required_keys = ["username", "pass", "passconfirm"]
        if not validate_form(request.form, required_keys):
            return render_template("register.html", message="Malformed request.", category="danger")

        username = request.form["username"]
        password = request.form["pass"]
        password_confirm = request.form["passconfirm"]

        if not username.isalnum():
            return render_template("register.html", message="Usernames must contain only alphanumeric characters.", category="danger")

        if password != password_confirm:
            return render_template("register.html", message="Passwords do not match.", category="danger")

        if user.get_user(username=username):
            return render_template("register.html", message="Username is already in use.", category="danger")

        user.add_user(username, password)

        return render_template("register.html", message="Account created!", category="success")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # User has submitted a request to login
        required_keys = ["username", "pass"]
        if not validate_form(request.form, required_keys):
            return render_template("login.html", message="Malformed request.", category="danger")

        username = request.form["username"]
        password = hashlib.sha1(request.form["pass"]).hexdigest()

        result = user.get_user(username=username)
        if result:
            if result[2] == password:
                session["username"] = username
                return redirect(url_for("index"))
            return render_template("login.html", message="Invalid password", category="danger")
        return render_template("login.html", message="Username does not exist...", add_mess="Register a new account?", category="danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

#to check if uploaded file is an image
extensions = set(['png','jpg','jpeg','PNG','JPG','JPEG'])
def checkFile(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in extensions

#generate either html for user to upload image OR to save uploaded image
@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method == "GET":
        return render_template("upload.html",upload="True")
    elif request.method == "POST":
        file = request.files['file']
        if file and checkFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(path,filename))
            return render_template("index.html",username=session['username'],message="Image Uploaded!",category="success")
        return render_template("upload.html",upload="True",message="Invalid File",category="danger")


if __name__=="__main__":
    if not os.path.exists("data.db"):
        db_builder.create_tables()
    app.debug = True

    # Generate and store secret key if it doesn't exist
    with open(".secret_key", "a+b") as f:
        secret_key = f.read()
        if not secret_key:
            secret_key = os.urandom(64)
            f.write(secret_key)
            f.flush()
        app.secret_key = secret_key

    app.run()
