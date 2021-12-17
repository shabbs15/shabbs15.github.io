from flask import Flask, render_template, request, redirect, url_for, session
import requests as req

app = Flask(__name__)
app.secret_key = "hello"

posts = [
    {
        "author": "Corey Schafer",
        "title": "blog post 1",
        "content": "first post content",
        "date_posted": "April 20, 2018"
    },
    {
        "author": "Jane Doe",
        "title": "ecomerce",
        "content": "check out this ecommers",
        "date_posted": "January 24, 2014"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/login", methods=["POST", "GET"])
def login():
    print("loginging in")
    if request.method=="POST":
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user", usr=user))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html", title="login")

@app.route("/user")
def user():
    if  "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/ip")
def ip():
    ip = request.headers.getlist("X-Forwarded-For")[0]
    ip = ip.split(":")[0]

    r = req.get("http://ipinfo.io/"+ ip).json() # "151.101.193.69"
    if not r["bogon"]:
        return r["city"] +", " + r["country"] + " this you? <br><br> Sorry this is saved mon ami, better chance next time"
    else:
        return "yo? odd" + request.remote_addr + ip

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)