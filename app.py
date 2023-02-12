#!/usr/bin/python
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
db_filename = "sqlite:///{}".format(os.path.join(project_dir, "books.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(100), nullable=False)

@app.route("/profile/<username>")
def guest(username):
    return render_template("profile.html", username=username)

@app.route("/profile/admin")
def admin():
    return "<h1> hi admin </h1>"

@app.route("/home/<name>")
def home(name):
    if name == "admin":
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("guest", username=name))

@app.route("/request")
def request_print():
    return "this is a request header{}".format(request.headers)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status/<username>")
def status(username):
    return render_template("show_status.html", isactive=True, username=username)

@app.route("/books")
def for_loop():
    # books = [{"Name":"malgudi days", "Author" : "R K Narayan", "cover" : "https://cdn.exoticindia.com/images/products/original/books/rk_narayans_malgudi_days_volume_hindi_dvd_video_icl082.jpg"},
    #         {"Name" : "Trancendence" , "Author" : "APJ Abdul Kalam", "cover" : "https://www.madrasshoppe.com/56603-large_default/transcendence-my-spiritual-experiences-with-pramukh-swamiji-1-edition-6-july-2015-a-p-j-abdul-kalam.jpg"},
    #         {"Name" : "Simply Fly", "Author": "Captain Gopinath", "cover" : "https://m.media-amazon.com/images/I/51gN98qcqKL._SY264_BO1,204,203,200_QL40_FMwebp_.jpg"}]
    books = Book.query.all()
    return render_template("books.html", books=books)

@app.route("/addbook")
def add_book():
    return render_template("addbook.html")

@app.route("/updatebook")
def updatebook():
    books = Book.query.all()
    return render_template("updatebook.html", books=books)

@app.route("/update", methods= ["POST"])
def update():
    oldname = request.form["oldname"]
    new_name = request.form["newname"]
    new_author = request.form["newauthor"]
    book = Book.query.filter_by(name=oldname).first()
    book.name = new_name
    book.author = new_author
    db.session.commit()
    return redirect('/books')

@app.route("/delete", methods= ["POST"])
def delete():
    new_name = request.form["newname"]
    book = Book.query.filter_by(name=new_name).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')

@app.route("/submitbook", methods = ["POST"])
def submitbook():
    book = Book(name=request.form["Name"], author=request.form["Author"])
    db.session.add(book)
    db.session.commit()
    return redirect('/books')

if __name__ == "__main__":
    app.run(debug=True)