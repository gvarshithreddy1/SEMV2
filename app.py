from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import csv
from methods import *

app = Flask(__name__)
cluster = MongoClient('mongodb+srv://gvarshithreddy8:Varshith1@cluster0.xzgxe3m.mongodb.net/?retryWrites=true&w=majority')

db = cluster.sem
studentdata = db.studentdata

if "studentyear" not in db.list_collection_names():
    studentyear = db.create_collection("studentyear")
else:
    studentyear = db.studentyear
    
#new code
year1 = studentyear.find_one(1)
try:
    students = year1['branches'][0]['sections'][0]['students']
except KeyError or NameError:
    print("No students uploaded yet in the requested branch and section")
# else:
#     for student in students:
#         print(student)
#new code end

@app.route("/")
def home():
    return render_template("home.html", title = "SEM")
'''
@app.route("/admin")
def admin():
    return render_template("admin.html", studentdetails = students)
'''
@app.route("/data", methods = ['POST','GET'])
def data():
    if request.method == 'GET':
        return f"The page /data was accessed directly, please submit the data in /admin first"
    elif request.method =='POST':
        form_data = request.form
        for i in form_data['name']:
            print(i)
        studentdetails_updated ={}
        len1 = len(form_data)
        limit = len1//2
        for i in range(limit):
            #studentdetails_updated[form_data[limit+i][1]] = form_data[i][1] 
            pass
        print(studentdetails_updated)
            
            
    return render_template("admin.html", studentdetails = studentdetails_updated)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return 'No file uploaded'

        file = request.files['csvFile']

        if file.filename == '':
            return 'No file selected'

        if file and allowed_file(file.filename):
            # Process the uploaded file
            process_csv(file)

            # Redirect to a success page or render a success template
            return render_template('admin.html',file_uploaded = True)

    return render_template('admin.html')







if __name__ == '__main__':
    app.run()

app.run(debug=True)