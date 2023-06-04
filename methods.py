import csv
from pymongo import MongoClient

def add_students_many(year, branch, section, csv_file):
    # Connect to MongoDB Atlas cluster
    # Replace <cluster_uri> with your actual MongoDB Atlas connection string
    cluster_uri = "mongodb+srv://gvarshithreddy8:Varshith1@cluster0.xzgxe3m.mongodb.net/?retryWrites=true&w=majority"
    cluster = MongoClient(cluster_uri)

    # Access the SEM database with the correct casing
    db = cluster.sem  # Replace "SEM" with the correct casing of the existing database

    # Access the studentyear collection
    studentyear = db.studentyear

    # Find the matching section in the studentyear collection
    year_document = studentyear.find_one({'_id': year})
    if year_document is None:
        print(f"Year {year} does not exist in the database.")
        cluster.close()
        return
    
    branch_documents = year_document['branches']
    matching_branch = next((b for b in branch_documents if b['branch'] == branch), None)
    if matching_branch is None:
        print(f"Branch {branch} does not exist in Year {year}.")
        cluster.close()
        return
    
    section_documents = matching_branch['sections']
    matching_section = next((s for s in section_documents if s['section'] == section), None)
    if matching_section is None:
        print(f"Section {section} does not exist in Branch {branch} of Year {year}.")
        cluster.close()
        return

    # Parse the CSV file and append studentdata documents to the section
    studentdata_collection = db.studentdata
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            rollno, studentname = row
            student = {
                'rollno': int(rollno),
                'studentname': studentname
            }
            
            # Append the student document to the respective section
            matching_section.setdefault('students', []).append(student)
    
    studentyear.replace_one({'_id': year}, year_document)
    print("Students added successfully.")

    # Close the MongoDB connection
    cluster.close()

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
