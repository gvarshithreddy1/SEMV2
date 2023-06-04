from flask import Flask, render_template
#from flask_pymongo import PyMongo

app = Flask(__name__)
#mongo = PyMongo(app)

@app.route("/home")
def home():
    return render_template("home.html")

app.run(debug=True)