from flask import Flask
from flask import render_template
import zugreifer

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("startpage.html")
@app.route("/home")
def home1():
    return "Hallo"
@app.route("/restaurant")
def home2():
    return render_template('speisekarte.html', items=zugreifer.getItemsVonSpeisekarte(zugreifer.getSpeisekarte(1)))