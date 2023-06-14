from flask import Flask, render_template, request, redirect, url_for,session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import random
import json
from flask_socketio import SocketIO, emit
import shutil
import ast
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import time

app = Flask(__name__)
app.secret_key = "jvictory2570"
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'jvictory2570'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_BINDS"] = {"user": "sqlite:///user.db"}

# MAIL SERVER
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "jvictory2570@gmail.com"
app.config["MAIL_PASSWORD"] = "faopnkfslqhfafvn"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

db = SQLAlchemy(app)
mail = Mail(app)
CORS(app)

# Define the BlogPost model
class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	article = db.Column(db.String(100), nullable=False)
	date_time = db.Column(db.String, nullable=False)
	author = db.Column(db.String(20), nullable=False)
	img_path = db.Column(db.String)
	post_likes = db.Column(db.String)

# Define the User_signup model
class User_signup(db.Model):
	_bind_key_ = "user"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String, default="User"+str(id))
	last_name = db.Column(db.String, nullable=False)
	user_name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	user_dp = db.Column(db.String, nullable=False)
	user_bio = db.Column(db.String, nullable=False)

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
		passwordc = request.form["passwordc"]

		if user_name[0] != "@":
			user_name = "@" + user_name

		email = request.form["email"]
		password = request.form["password"]
		user_dp = request.form["user_p"]
		hashed_password = generate_password_hash(password)

		for u_e in range(len(users_d)):
			users_email.append(users_d[u_e].email)

		error = ""
		if password != passwordc:
			error = "passwords do not match"
			return render_template("signup.html", error=error)

		if email in users_email:
			error = "User already exists"
			return render_template("signup.html", error=error)
		else:
			new_user = User_signup(first_name=first_name, last_name=last_name, user_name=user_name,
								   email=email, password=hashed_password, user_dp=url_for('static',filename = "user.png"),user_bio = "Add a bio?")

			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('log_in'))
	else:
		return render_template("signup.html")

# Log in route
@app.route("/thescienceforum/login", methods=["GET", "POST"])
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

					session ["profile_pic"] = profile_pic
					session ["un"] = username
					session ["uid"] = user_id
					return redirect(url_for("user_page")), user_id

			if len(pass_l) == len(true_checker):
				if True not in true_checker:
					error1 = "Invalid credentials"
					return render_template("login.html", error1=error1)
		else:
			error1 = "User not found"
			return render_template("login.html", error1=error1)

	else:
		return render_template("login.html")

# User page route
@app.route("/userpage", methods=["GET", "POST"])
def user_page():
	#like = request.json.get("data")
	#print(like)
	@socketio.on('like-data')
	def like(like_data):
		
		post_id = int(like_data[1])
		user_like_email = like_data[0]
		like_event = like_data[2]
		
		new_dict = {}
		post_like_data = db.session.query(BlogPost).filter_by(id = post_id).first()
		con_dict = ast.literal_eval(post_like_data.post_likes)
		
		if post_id in con_dict:
			user_c = con_dict[post_id]
			if user_like_email in user_c:
				con_dict[post_id][user_like_email] = like_event
				print(con_dict)
				post_like_data.post_likes = str(con_dict)
				db.session.commit()
			else:
				u_d = {user_like_email:like_event}
				con_dict[post_id].update(u_d)
				post_like_data.post_likes = str(con_dict)
				db.session.commit()
				
		else:
			new_dict[post_id] = {user_like_email:like_event}			
			post_like_data.post_likes = str(new_dict)
			db.session.commit()
			
		response = {'message': 'Data received successfully'}
		emit('response', response)
	
	un = session.get("un")
	uid = session.get("uid")

	db_data = db.session.query(User_signup).all()
	bp_data = db.session.query(BlogPost).all()
	prof_pic_data = db.session.query(User_signup).filter_by(id=uid).first()
	prof_pic = prof_pic_data.user_dp
	user_pic = prof_pic

	profile_pic = session.get("profile_pic")
	data_get = db.session.query(User_signup).filter_by(id=uid).first()

	user_fname = data_get.first_name
	user_sname = data_get.last_name
	username = data_get.user_name

	post_content = request.form.get("content")
	post_content1 = request.form.get("content1")
	add_photo_name = request.form.get("filename")
	
	j_d = "{}"
	if request.method == "POST":
		print (post_content,post_content1,add_photo_name)

		if post_content != None:
			new_post = BlogPost(user_id = uid, article = post_content, date_time = datetime.date.today(), author = user_fname+" "+user_sname, img_path = None,post_likes = j_d)

			db.session.add(new_post)
			db.session.commit()

			return redirect(url_for("user_page"))

		elif post_content1 != None:
			if add_photo_name != None:
				image_upload = request.files["image_upload"]
				new_post = BlogPost(user_id = uid, article = post_content1, date_time = datetime.date.today(), author = user_fname+" "+user_sname, img_path = url_for('static',filename=image_upload.filename),post_likes = j_d)

				db.session.add(new_post)
				db.session.commit()
				return  redirect (url_for("user_page"))

		else:
			return redirect (url_for("user_page"))
	else:
		post_list = []
		post_db = db.session.query(BlogPost).all()
		for post_dbv in post_db:
			post_list.append(ast.literal_eval(post_dbv.post_likes))
						
		return render_template("user_page.html", uid=uid, db_data=db_data, un=un, user_pic = user_pic,bp_data = bp_data,post_list = post_list), un

email_list = []
db_data = db.session.query(User_signup).all()
for dbd in range(len(db_data)):
	email_list.append(db_data[dbd].email)

an = random.randint(90000,1000000)
an1 = random.randint(90000,1000000)

#forgot pass route
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

	if request.method == "POST":
		reset_code = random.randint(90000,1000000)
		msg = ""
		strc = str(reset_code)

		user_email = request.form["email"]
		msg = Message("Reset Password", sender='jvictory2570@gmail.com',recipients=[user_email])
		msg.body = f'We are sorry to here that you forgot your password, your password reset code is {strc}'

		reset_code = ""
		for lent in range(len(strc)):
			reset_code +=strc[lent]
		#print(reset_code)

		if user_email in email_list:
			mail.send(msg)
			session["c_email"] = user_email

			return redirect(url_for("reset_code",an = an,reset_code = reset_code,an1 = an1))
		else:
			return render_template("forgotPassword.html", msg="Email entered does not exist")

	else:
		return render_template("forgotPassword.html")

#reset code route
@app.route("/code/<an>/<reset_code><an1>", methods=["GET","POST"])
def reset_code(an,reset_code,an1):
	msg = ""
	r_code = str(reset_code)[:6]
	#print(r_code)

	if request.method == "POST":
		code = request.form["code"]
		#print("new",reset_code,"code",code)

		if str(code) == r_code:
			return redirect(url_for("new_password"))
		else:
			return render_template("reset_password.html",an = an,reset_code = reset_code,msg = "Incorrect code")

	else:
		return render_template("reset_password.html",an = an, reset_code = reset_code)

#new password route
@app.route("/new_password", methods=["GET","POST"])
def new_password():

	user_email = session.get("c_email")
	db_e = db.session.query(User_signup).filter_by(email = user_email).first()

	if request.method == "POST":
		new_user_pass = request.form["password"]

		new_pass = generate_password_hash(new_user_pass)
		db_e.password = new_pass

		db.session.commit()
		return redirect(url_for("log_in"))

	else:
		return render_template("new_password.html")

# Edit profile route
@app.route("/editProfile", methods=["GET", "POST"])
def edit_profile():
	rand_int = 5

	un = session.get("un")
	uid = session.get("uid")

	user_data = db.session.query(User_signup).all()
	prof_pic_data = db.session.query(User_signup).filter_by(id=uid).first()
	prof_pic = prof_pic_data.user_dp
	user_pic = prof_pic

	if request.method == "POST":
		firstname = request.form.get("firstname")
		lastname = request.form.get("lastname")

		u_bio = request.form.get("u_bio")
		username_ = request.form.get("username")

		if username_[0] != "@":
			username_ = "@" + username_
		
		image_uploadb = request.files["image_upload"]
		image_uploadb.save("/storage/emulated/0/bp/static/"+image_uploadb.filename)
		
		password = request.form.get("password")
		email = request.form.get("email")
		user_pp = request.form.get("userpp")
		t_c = []
		pass_list = []
		db_data = db.session.query(User_signup).all()		
			
		if firstname!="":
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
					user.user_bio = u_bio
					user.user_dp = url_for('static',filename = image_uploadb.filename)

					db.session.commit()
					return redirect(url_for("user_page"))

				if len(pass_list) == len(db_data):
					if True not in t_c:
						return render_template("editProfile.html", user_data=user_data, uid=uid, un=un,user_pic=user_pic,
										   error="Incorrect password")
	else:
		return render_template("editProfile.html", user_data=user_data, uid=uid, un=un, user_pic=user_pic), uid

#user profile route
@app.route("/my-profile", methods=["GET","POST"])
def my_profile():
	uid = session.get("uid")
	db_data = db.session.query(User_signup).all()
	bp_data = db.session.query(BlogPost).all()
	user_db = db.session.query(User_signup).filter_by(id = uid).first()

	if request.method == "POST":
		return "ok"
	else:
		return render_template("my-profile.html",uid=uid,user_db = user_db,db_data = db_data, bp_data = bp_data)

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

		db.session.add(new_post)
		db.session.commit()
		return redirect("/main")
	else:
		data = db.session.query(BlogPost).all()
		return render_template("base.html", data=data)

if __name__ == "__main__":
	app.run(debug=True)