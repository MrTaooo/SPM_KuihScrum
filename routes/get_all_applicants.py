from flask import request, jsonify
from sqlalchemy import *
from models.job_application import JobApplication
from models.staff import Staff

def get_applicants(joblist_ID):
    # retrieve the applicants for the job listing
    applicants = JobApplication.query.filter_by(JobList_ID=joblist_ID).all()

    # create a dictionary to store the applicant details for each job listing 
    applicant_list = []

    if applicants is None:
        return jsonify({
            "code": 404, 
            "message": "No applicants found for this job listing."
        })
    else:
        for applicant in applicants:
            # retrieve the staff information from Staff table using the Staff_ID
            Staff_Info = Staff.query.filter_by(Staff_ID=applicant.Staff_ID).first().json()
            applicant_list.append(Staff_Info)
        return jsonify({
            "code": 200, 
            "data": {
                    "applicants": applicant_list
                }
        })