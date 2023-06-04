from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONOGO_URI"] = "mongodb+srv://gvarshithreddy8:<password>@cluster0.xzgxe3m.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app)
@app.route("/")
def home():
    return render_template("home.html")

app.run(debug=True)