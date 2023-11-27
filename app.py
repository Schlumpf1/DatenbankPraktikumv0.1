from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("startpage.html")
@app.route("/home")
def home():
    return "Hallo"