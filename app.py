from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import csv,os
from methods import *

years = [1,2,3,4]
branches = ['CSE', 'IT', 'AIDS', 'AIML', 'Chemical Engineering', 'Civil', 'Mechanical', 'ECE', 'EEE']
sections =["Section 1","Section 2","Section 3"]

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



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get the selected values from the form
        year = int(request.form.get('year'))
        branch = str(request.form.get('branch'))
        section = str(request.form.get('section'))
        

        

        if 'csvFile' not in request.files:
            return 'No file uploaded'

        file = request.files['csvFile']

        if file.filename == '':
            return 'No file selected'

        if file and allowed_file(file.filename):
            print(section)
            print("ESXRCDTVFGBHJNK MSRDCTVFBJNKMDCTFVYGBUHNIJMOK<DCTFVYGBUHNIJMCTFVYGBUHN")
            file_path = save_uploaded_file(file)
            # Pass the selected values and the file to the add_students_many method
            add_students_many(cluster,year, branch, section, file_path)
            os.remove(file_path)

            # Redirect to a success page or render a success template
            return 'File uploaded and processed successfully'

    return render_template('admin.html',years = years,branches=branches,sections= sections )


def save_uploaded_file(file):
    # Save the uploaded file to a temporary location
    temp_folder = 'temp'
    os.makedirs(temp_folder, exist_ok=True)
    file_path = os.path.join(temp_folder, file.filename)
    file.save(file_path)
    return file_path





if __name__ == '__main__':
    app.run()

app.run(debug=True)