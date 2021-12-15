from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)