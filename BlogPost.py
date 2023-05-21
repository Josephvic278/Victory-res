from flask import Flask, render_template, request, redirect, url_for, make_response
import urllib 
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import shutil
from  werkzeug.security import  generate_password_hash,check_password_hash
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config["SQLALCHEMY_BINDS"] = {"user":"sqlite:///user.db" }

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    img_path = db.Column(db.String)

class User_signup(db.Model):
	__bind_key__ = "user"
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String, default="User"+str(id))
	last_name = db.Column(db.String, nullable=False)
	user_name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable = False)
	user_dp = db.Column(db.String, nullable=False)
	
#checks if database exists
list_dir = os.listdir()
if "main.db" and "user.db"not in list_dir:
    app.app_context().push()
    db.create_all()

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/t_s_f/sign_up", methods=["GET","POST"])
def sign_up():
	users_d = db.session.query(User_signup).all()
	if request.method == "POST":
		users_email = []
		
		first_name = request.form["firstname"]
		last_name = request.form["lastname"]
		user_name = request.form["username"]
		if user_name[0]!="@":
			user_name = "@"+user_name
			
		email = request.form["email"]
		password = request.form["password"]
		user_dp = request.form["user_p"]
		hashed_password = generate_password_hash(password)
		
		for u_e in range(len(users_d)):
			users_email.append(users_d[u_e].email)
		
		error = ""
		if email in users_email:
			error = "User already exists"
			
			return render_template("signup.html",error = error)
		
		else:
			new_user = User_signup(first_name=first_name,last_name=last_name,user_name=user_name,email=email,password=hashed_password,user_dp = "user.png")
		
			db.session.add(new_user)
			db.session.commit()
			return redirect("/t_s_f/log_in")
	else:
		return render_template("signup.html")

@app.route("/t_s_f/log_in", methods=["GET","POST"])
def log_in():
	
	email_list1 = []
	vrd = []
	#this doesthisjdjdjdj
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
		
		#ind_p = email_list1.index(str(email_address))
		true_checker = []
		
		if email_address in email_list1:
			for db_data in range(len(log_data)):
				
				password_authentecator = check_password_hash(pass_l[db_data],password)
				true_checker.append(password_authentecator)
				
				if password_authentecator == True:
					user_id = log_data[db_data].id
					username = log_data[db_data].user_name
					profile_pic = log_data[db_data].user_dp
					print(password_authentecator)
					
					return redirect (url_for("user_page",un=username,uid = user_id,profile_pic = profile_pic)),user_id
				
				if len(pass_l) == len(true_checker):
					if True not in true_checker:
						error1="Invalid credentials"
						return render_template("login.html", error1=error1)
		else:
			error1 = "User not found"
			return render_template("login.html",error1 = error1)
		
		#return redirect ("/t_s_f/log_in")
	
	else:
		return render_template("login.html")
		
@app.route("/userpage/<un>/<int:uid>/<profile_pic>/user_", methods=["GET","POST"])
def user_page(un,uid, profile_pic):
	db_data = db.session.query(User_signup).all()
	
	pic_url = url_for('static',filename=profile_pic)
	if request.method == "POST":
		return "ok"
	else:
		return render_template("user_page.html",uid=uid,db_data = db_data,un=un,pic_url = pic_url),un

@app.route("/editProfile/<int:uid>/<un>/", methods=["GET","POST"])
def edit_profile(uid,un):
	user_data = db.session.query(User_signup).all()
	prof_pic_data = db.session.query(User_signup).filter_by(id=uid).first()
	prof_pic = prof_pic_data.user_dp
	user_pic = url_for('static',filename=prof_pic)
	
	if request.method == "POST":
		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		username_ = request.form["username"]
		if username_[0]!="@":
			username_ = "@"+username_
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
			if pass_aunth == True:			
				
				user = db.session.query(User_signup).filter_by(id=uid).first()
				
				user.first_name = firstname
				user.last_name = lastname 
				user.user_name = username_
				user.email = email

				if user_pp!="":
					if os.name == "nt":
						win_download_folder = os.path.join(os.environ['USERPROFILE'],'Downloads')
					
					elif os.name == "posix":
						and_linux_download_folder = os.path.join(os.path.expanduser('~'),'Downloads')
						print(and_linux_download_folder)
						
						get_and_list = os.listdir(and_linux_download_folder)
						
						if user_pp in get_and_list:
							print("file exists")
				
				db.session.commit()
				return redirect(url_for("user_page",un=un,uid=uid, profile_pic=prof_pic))
				
			if len(pass_list) == len(db_data):
				if True not in t_c:
		
					return render_template("editProfile.html",user_data = user_data,uid=uid,un=un,error = "Incorrect password")
				
					
	else:
		return render_template("editProfile.html",user_data = user_data,uid=uid,un=un,user_pic = user_pic)

@app.route("/main", methods=["GET","POST"])
def create_post():
	if request.method=="POST":
		title = request.form["title"]
		article = request.form["content"]
    
		date_time = str(datetime.date.today()) + " " + time.strftime("%H:%M:%S")
		author = request.form["author"]
		img_path = request.form["img"]
		new_post = BlogPost(title=title, article=article, 							date_time=date_time, author=author,img_path=img_path)

		print(img_path)
		print(os.getcwd())
		db.session.add(new_post)
		db.session.commit()
		return redirect("/main")
	else:
		data = db.session.query(BlogPost).all()
		return render_template("base.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)
