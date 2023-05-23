from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import random
import shutil
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_BINDS"] = {"user": "sqlite:///user.db"}
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "jvictory2570"
app.config['MAIL_PASSWORD'] = "animation1978"

db = SQLAlchemy(app)
mail = Mail(app)

# Define the BlogPost model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    img_path = db.Column(db.String)

# Define the User_signup model
class User_signup(db.Model):
    __bind_key__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, default="User"+str(id))
    last_name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_dp = db.Column(db.String, nullable=False)

# Check if the database exists
list_dir = os.listdir()
if "main.db" not in list_dir and "user.db" not in list_dir:
    app.app_context().push()
    db.create_all()

# Main page route
@app.route("/")
def main():
    return render_template("main.html")

# Sign up route
@app.route("/t_s_f/sign_up", methods=["GET", "POST"])
def sign_up():
    users_d = db.session.query(User_signup).all()
    if request.method == "POST":
        users_email = []
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        user_name = request.form["username"]
        
        if user_name[0] != "@":
            user_name = "@" + user_name
        
        email = request.form["email"]
        password = request.form["password"]
        user_dp = request.form["user_p"]
        hashed_password = generate_password_hash(password)
        
        for u_e in range(len(users_d)):
            users_email.append(users_d[u_e].email)
        
        error = ""
        if email in users_email:
            error = "User already exists"
            return render_template("signup.html", error=error)
        else:
            new_user = User_signup(first_name=first_name, last_name=last_name, user_name=user_name,
                                   email=email, password=hashed_password, user_dp="user.png")
            db.session.add(new_user)
            db.session.commit()
            return redirect("/t_s_f/log_in")
    else:
        return render_template("signup.html")

# Log in route
@app.route("/t_s_f/log_in", methods=["GET", "POST"])
def log_in():
    rand_int = ""
    for rand in range(6):
        rand_int_g = random.randint(1, 10)
        rand_int += str(rand_int_g)
    
    email_list1 =[]
    vrd = []
    log_data = db.session.query(User_signup).all()
    for email_list in range(len(log_data)):
        email_list1.append(log_data[email_list].email)
        vrd.append(log_data[email_list].password)
    
    error1 = ""
    pass_l = []
    
    for pl in range(len(log_data)):
        pass_l.append(log_data[pl].password)
    
    if request.method == "POST":
        email_address = request.form["email"]
        password = request.form["password"]
        true_checker = []
        
        if email_address in email_list1:
            for db_data in range(len(log_data)):
                password_authenticator = check_password_hash(pass_l[db_data], password)
                true_checker.append(password_authenticator)
                
                if password_authenticator:
                    user_id_data = db.session.query(User_signup).filter_by(email=email_address).first()
                    user_id = user_id_data.id
                    username_data = db.session.query(User_signup).filter_by(email=email_address).first()
                    username = username_data.user_name
                    profile_pic = log_data[db_data].user_dp
                    return redirect(url_for("user_page", un=username, uid=user_id, profile_pic=profile_pic,
                                            rand_int=rand_int)), user_id
                
            if len(pass_l) == len(true_checker):
                if True not in true_checker:
                    error1 = "Invalid credentials"
                    return render_template("login.html", error1=error1), user_id
        else:
            error1 = "User not found"
            return render_template("login.html", error1=error1)
    
    else:
        return render_template("login.html")

# User page route
@app.route("/userpage/<un>/<rand_int><int:uid>/<profile_pic>/user_", methods=["GET", "POST"])
def user_page(un, uid, profile_pic, rand_int):
    db_data = db.session.query(User_signup).all()
    data_get = db.session.query(User_signup).filter_by(id=uid).first()
    p_pic = data_get.user_dp
    pic_url = url_for('static', filename=p_pic)
    
    if request.method == "POST":
        return "ok"
    else:
        return render_template("user_page.html", uid=uid, db_data=db_data, un=un, pic_url=pic_url), un

email_list = []
db_data = db.session.query(User_signup).all()
for dbd in range(len(db_data)):
    email_list.append(db_data[dbd].email)

# Forgot password route
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    
    if request.method == "POST":
        msg = ""
        
        user_email = request.form["email"]
        msg = Message('Hello', sender='jvictory2570@gmail.com',recipients=[user_email])
        msg.body = "This is the body of the email."
        
        if user_email in email_list:
            mail.send(msg)
            return redirect(url_for("forgot_password"))
        else:
            return render_template("forgotPassword.html", msg="Email entered does not exist")
    
    else:
        return render_template("forgotPassword.html")

# Edit profile route
@app.route("/editProfile/<int:uid>/<un>/", methods=["GET", "POST"])
def edit_profile(uid, un):
    user_data = db.session.query(User_signup).all()
    prof_pic_data = db.session.query(User_signup).filter_by(id=uid).first()
    prof_pic = prof_pic_data.user_dp
    user_pic = url_for('static', filename=prof_pic)
    
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]


        username_ = request.form["username"]
        
        if username_[0] != "@":
            username_ = "@" + username_
        
        password = request.form["password"]
        email = request.form["email"]
        user_pp = request.form["userpp"]
        t_c = []
        pass_list = []
        db_data = db.session.query(User_signup).all()
        
        for udb in range(len(db_data)):
            pass_list.append(db_data[udb].password)
            pass_aunth = check_password_hash(db_data[udb].password, password)
            t_c.append(pass_aunth)
            
            if pass_aunth:
                user = db.session.query(User_signup).filter_by(id=uid).first()
                user.first_name = firstname
                user.last_name = lastname
                user.user_name = username_
                user.email = email
                
                if user_pp != "":
                    if os.name == "nt":
                        win_download_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
                    elif os.name == "posix":
                        and_linux_download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
                        print(and_linux_download_folder)
                        
                        get_and_list = os.listdir("/storage/emulated/0/Download")
                        download_dir = "/storage/emulated/0/Download/"
                        file_name = download_dir + "/" + user_pp
                        
                        if user_pp in get_and_list:
                            print("file exists")
                            shutil.copy(file_name, os.getcwd() + "/" + "static")
                            user.user_dp = user_pp
                
                db.session.commit()
                return redirect(url_for("user_page", un=un, uid=uid, profile_pic=prof_pic))
            
            if len(pass_list) == len(db_data):
                if True not in t_c:
                    return render_template("editProfile.html", user_data=user_data, uid=uid, un=un,
                                           error="Incorrect password")
    else:
        return render_template("editProfile.html", user_data=user_data, uid=uid, un=un, user_pic=user_pic), uid

# About us route
@app.route("/aboutUs", methods=["GET", "POST"])
def about_us():
    if request.method == "POST":
        return "ok"
    else:
        return render_template("aboutUs.html")

@app.route("/main", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        article = request.form["content"]
        date_time = str(datetime.date.today()) + " " + time.strftime("%H:%M:%S")
        author = request.form["author"]
        img_path = request.form["img"]
        new_post = BlogPost(title=title, article=article, date_time=date_time, author=author, img_path=img_path)
        
        print(img_path)
        print(os.getcwd())
        db.session.add(new_post)
        db.session.commit()
        return redirect("/main")
    else:
        data = db.session.query(BlogPost).all()
        return render_template("base.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)