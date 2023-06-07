import csv
from pymongo import MongoClient
import random

def add_students_many(cluster, year, branch, section, csv_file):
    # Connect to MongoDB Atlas cluster
    # Replace <cluster_uri> with your actual MongoDB Atlas connection string

    # Access the SEM database with the correct casing
    db = cluster.sem  # Replace "SEM" with the correct casing of the existing database

    # Access the studentyear collection
    studentyear = db.studentyear

    # Find the matching section in the studentyear collection
    year_document = studentyear.find_one({'_id': year})
    if year_document is None:
        print(f"Year {year} does not exist in the database.")
        return
    
    branch_documents = year_document['branches']
    matching_branch = next((b for b in branch_documents if b['branch'] == branch), None)
    if matching_branch is None:
        print(f"Branch {branch} does not exist in Year {year}.")
        return
    
    section_documents = matching_branch['sections']
    matching_section = next((s for s in section_documents if s['section'] == section), None)
    if matching_section is None:
        print(f"Section {section} does not exist in Branch {branch} of Year {year}.")
        return

    # Parse the CSV file and create a list of student documents
    students = []
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            rollno, studentname = row
            student = {
                'rollno': int(rollno),
                'studentname': studentname
            }
            
            students.append(student)

    # Update the section with the new list of student documents
    matching_section['students'] = students

    # Replace the section in the studentyear collection
    studentyear.replace_one({'_id': year}, year_document)
    print("Students added successfully.")


    # Close the MongoDB connection
    #

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def process_csv(file):
    # Process the uploaded CSV file
    # Here, you can write your code to parse and handle the CSV data
    # For example, you can use the csv module to read the file contents
    csv_reader = csv.reader(file.read().decode('utf-8').splitlines())
    for row in csv_reader:
        # Process each row of the CSV data
        # You can access the row values using row[0], row[1], etc.
        pass

def get_students(yearcollection,Year=None,branch=None,section=None):
    ('cse',)
    years = yearcollection.find()
    branches = ['CSE', 'IT', 'AIDS', 'AIML', 'Chemical Engineering', 'Civil', 'Mechanical', 'ECE', 'EEE']
    
    for i in range(len(branches)):
        if branch.lower() == branches[i].lower():
            branchcode = i

    try:
        studentyears = list(years)
    except KeyError or NameError:
        print("No students uploaded yet in the requested branch and section")
    else:
        year = studentyears[Year-1]
        return year['branches'][branchcode]['sections'][section-1]['students']

def get_branches(studentyear,year):

    year1 = studentyear.find_one(year)

    
    branches = year1['branches']
    b = []
    for i in range(len(branches)):
        
        b.append(branches[i]['branch'])

    return b


def allocate_students(num_experiments, student_data):
    # Shuffle the student data randomly
    random.shuffle(student_data)

    # Calculate the number of students per experiment
    students_per_experiment = len(student_data) // num_experiments

    # Initialize the experiment allocation results
    experiments = [[] for _ in range(num_experiments)]

    # Allocate students to experiments
    for i in range(num_experiments):
        # Get students for the current experiment
        start_index = i * students_per_experiment
        end_index = start_index + students_per_experiment
        experiment_students = student_data[start_index:end_index]

        # Add the experiment students to the corresponding experiment
        experiments[i].extend(experiment_students)

    # If there are any remaining students, allocate them randomly to experiments
    remaining_students = len(student_data) % num_experiments
    if remaining_students > 0:
        remaining_students_indices = random.sample(range(len(student_data)), remaining_students)
        for i, student_index in enumerate(remaining_students_indices):
            experiments[i].append(student_data[student_index])

    return experiments
