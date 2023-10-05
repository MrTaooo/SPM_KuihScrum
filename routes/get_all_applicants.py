from flask import request, jsonify
from sqlalchemy import *
from models.job_application import JobApplication
from models.staff import Staff

def get_applicants():
    # retrieve the applicants for the job listing
    applicants = JobApplication.query.all()

    # create a dictionary to store the applicant details for each job listing 
    applicant_dict = {}

    if applicants is None:
        return jsonify({
            "code": 404, 
            "message": "No applicants found for this job listing."
        })
    else:
        for applicant in applicants:
            # retrieve the staff information from Staff table using the Staff_ID
            Staff_Info = Staff.query.filter_by(Staff_ID=applicant.Staff_ID).first().json()
            # Check if the key exists in the dictionary, and if not, create an empty list
            if applicant.JobList_ID not in applicant_dict:
                applicant_dict[applicant.JobList_ID] = []

            # Append Staff_Info to the list associated with the key
            applicant_dict[applicant.JobList_ID].append(Staff_Info)
        return jsonify({
            "code": 200, 
            "data": {
                    "applicants": [applicant_dict]
                }
        })