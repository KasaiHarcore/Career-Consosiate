from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

mongo = PyMongo()


class MongoDBHandler:
    """
    Class to handle MongoDB operations with:
    - Inserting data
    - Finding data
    - Updating data
    - Deleting data
    """
    def __init__(self, uri, db_name):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            
            # Check if the collections exist, otherwise create them
            if 'resumes' not in self.db.list_collection_names():
                self.resume_collection = self.db.create_collection('resumes')
            else:
                self.resume_collection = self.db['resumes']

            if 'job_descriptions' not in self.db.list_collection_names():
                self.job_description_collection = self.db.create_collection('job_descriptions')
            else:
                self.job_description_collection = self.db['job_descriptions']
            
            print(f"Connected to database '{db_name}' successfully!")

        except errors.ConnectionFailure as cf:
            print(f"Connection error: {cf}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Insert Resume
    def insert_resume(self, resume_data):
        try:
            result = self.resume_collection.insert_one(resume_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting resume: {e}")

    # Insert Job Description
    def insert_job_description(self, job_data):
        try:
            result = self.job_description_collection.insert_one(job_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting job description: {e}")

    # Find Resume by criteria
    def find_resume(self, query):
        try:
            results = self.resume_collection.find(query)
            return list(results)
        except Exception as e:
            print(f"Error finding resume: {e}")

    # Find Job Description by criteria
    def find_job_description(self, query):
        try:
            results = self.job_description_collection.find(query)
            return list(results)
        except Exception as e:
            print(f"Error finding job description: {e}")

    # Update Resume by ID
    def update_resume(self, resume_id, updated_data):
        try:
            result = self.resume_collection.update_one(
                {'_id': ObjectId(resume_id)}, {'$set': updated_data}
            )
            return result.modified_count
        except Exception as e:
            print(f"Error updating resume: {e}")

    # Update Job Description by ID
    def update_job_description(self, job_id, updated_data):
        try:
            result = self.job_description_collection.update_one(
                {'_id': ObjectId(job_id)}, {'$set': updated_data}
            )
            return result.modified_count
        except Exception as e:
            print(f"Error updating job description: {e}")

    # Delete Resume by ID
    def delete_resume(self, resume_id):
        try:
            result = self.resume_collection.delete_one({'_id': ObjectId(resume_id)})
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting resume: {e}")

    # Delete Job Description by ID
    def delete_job_description(self, job_id):
        try:
            result = self.job_description_collection.delete_one({'_id': ObjectId(job_id)})
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting job description: {e}")
            
            
            
db_handler = MongoDBHandler('mongodb://localhost:27017/', 'my_database')

# Test (Error)
resume = {
    "ID": 16852973,
    "Resume": "HR ADMINISTRATOR/MARKETING ASSOCIATE...",
    "Category": "HR",
    "Education": {"University": "Jefferson College", "Major": "Business Administration"},
    "Achievements": [{"Description": "Missouri DOT Supervisor Training"}],
    "Skills": ["Accounting", "ads", "advertising", "analytics"],
    "Experience": [{"Job Title": "HR Administrator", "Company": "ABC Corp", "Years": 2}]
}
resume_id = db_handler.insert_resume(resume)

if resume_id:
    print("Resume inserted with ID:", resume_id)
else:
    print("Failed to insert resume")