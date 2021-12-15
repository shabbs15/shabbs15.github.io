from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hell, world"
    return render_template("index.html")