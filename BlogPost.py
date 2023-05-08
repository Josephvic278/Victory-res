from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String, nullable=False)
    author = db.Column(db.String(20), nullable=False)

#checks if database exists
list_dir = os.listdir()
if "main.db" not in list_dir:
    app.app_context().push()
    db.create_all()

@app.route("/")
def main():
    data = db.session.query(BlogPost).all()
    return render_template("base.html", data=data)

@app.route("/main", methods=["POST"])
def create_post():
    title = request.form["title"]
    article = request.form["content"]
    date_time = str(datetime.date.today()) + " " + time.strftime("%H:%M:%S")
    author = request.form["author"]
    new_post = BlogPost(title=title, article=article, date_time=date_time, author=author)
    db.session.add(new_post)
    db.session.commit()
    
    data = db.session.query(BlogPost).all()
    return render_template("base.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)
