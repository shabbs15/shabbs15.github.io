from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import model
model = model()
import requests as req
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        user = request.form["nm"]
        session["user"] = user
        flash("logged in, well done")
        return redirect(url_for("user"))
    else:
        return render_template("login.html", title="login")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", name=user)
    else:
        return redirect(url_for("login"))

@app.route("/wall", methods=["POST", "GET"])
def wall():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            if "post" in request.form:
                post = request.form["post"]
                date = datetime.today().strftime('%Y-%m-%d %H:%M')
                model.addToTheWall(post, user, date)
                return redirect(url_for("wall"))
            elif "key" in request.form and user == "shabbs":
                key = request.form["key"]
                model.deleteRecord(key)
                return redirect(url_for("wall"))
        
        wallPosts = model.getPosts()
        
        print("yo", user=="shabbs")

        return render_template("wall.html", posts=wallPosts, admin=user=="shabbs")
    else:
        return redirect(url_for("login"))

@app.route("/ip")
def ip():
    r = req.get("http://ipinfo.io/"+ ip).json() # "151.101.193.69"
    if not "bogon" in r:
        return r["city"] +", " + r["country"] + " this you? <br><br> Sorry this is saved mon ami, better chance next time"
    else:
        return "yo? odd" + request.remote_addr + ip

@app.route("/logout")
def logout():
    if "user" in session:   
        session.pop("user", None)
        flash("You have been logged out!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)