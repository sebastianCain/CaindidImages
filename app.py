from flask import abort, Flask, render_template, g, request, current_app, redirect, url_for, session, Blueprint
from flask_paginate import Pagination, get_page_args
import datetime, os, urllib, string
import sqlite3
from werkzeug.utils import secure_filename

import hashlib
import db_builder
import user
import glob
#import utils.clarifai

#path for upload folder
path = "images"
app = Flask(__name__)

def validate_form(form, required_keys):
    """ Check if a dictionary contains all the required keys """
    return set(required_keys) <= set(form)

@app.before_request
def before_request():
    g.conn = sqlite3.connect('data.db')
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()


@app.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        g.conn.close()



#login route
@app.route("/", methods=["POST", "GET"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    per_page = 5
    page, per_page, offset = get_page_args()
    sql = 'select path from pics order by path limit {}, {}'\
        .format(offset, per_page)
    g.cur.execute(sql)
    images = g.cur.fetchall()
    
    
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                record_name='images',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('index.html', images=images,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@app.route('/images/', defaults={'page': 1})
@app.route('/images', defaults={'page': 1})
@app.route('/images/page/<int:page>/')
@app.route('/images/page/<int:page>')
def images(page):
    per_page = 5
    page, per_page, offset = get_page_args()
    sql = 'select path from pics order by path limit {}, {}'\
        .format(offset, per_page)
    g.cur.execute(sql)
    images = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                record_name='images',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('index.html', images=images,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           active_url='images-page-url',
                           )
    #images = glob.glob("static/images/*")
    #ci = []
    #for i in images:
     #   ci.append(i[13:])


    
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
@app.route("/upload")
def upload_local():
    return render_template("upload.html",upload="True")

@app.route("/upload/local", methods=['POST'])
def local():
    file = request.files['file']
    if file and checkFile(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(path,filename))
        #tags = utils.clarifai.requestTags(filename)
        #Add tags to table- work in progress
        #add_pic(path+"/"+filename, uid????, tags)
        #a way to add tags one by one since the variable tags is a dict?
        uid = user.get_UID(session['username'])
        user.add_pic(os.path.join(path,filename),uid)
        return render_template("index.html",username=session['username'],message="Image Uploaded!",category="success")
    return render_template("upload.html",upload="True",message="Invalid File",category="danger")

@app.route("/upload/web", methods=['POST'])
def web():
    if checkFile(request.form['link']):
        ext = request.form['link'].rsplit('.',1)[1]
        response = urllib.urlopen(request.form['link'])
        image = response.read()
        filename = stripPunctuation(request.form['filename'])+"."+ext
        filename = repeatedName(filename,0,False)
        with open(path+"/"+filename,"wb") as out:
            out.write(image)
            return render_template("index.html",username=session['username'],message="Image Uploaded!", category="success")
    return render_template("upload.html",upload="True",message="Invalid File",category="danger")
def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def stripPunctuation(name):
    for p in string.punctuation:
        name=name.replace(p,"")
    return name

def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )


def repeatedName(name,num,looped):
    
    if name in os.listdir(path):
        if looped:
            name = name.rsplit('.',1)[0][:-(len(str(num)))]+"."+name.rsplit('.',1)[1]
        print name
        name = name.rsplit('.',1)[0]+str(num)+"."+name.rsplit('.',1)[1]
        num += 1
        print name + ", " + str(num)
        return repeatedName(name,num,True)
    return name

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
