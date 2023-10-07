from flask import request, jsonify
from models.job_application import JobApplication

def get_applied_jobs_for_user(staff_id):
    # retrieve all the job applications for the staff
    applied_jobs = JobApplication.query.filter_by(Staff_ID=staff_id).all()

    if applied_jobs is None:
        return jsonify({
            "code": 404, 
            "message": "No job applications found for this staff."
        })
    
    return jsonify({
        "code": 200,
        "data": {
            "appliedJobs": [job.JobList_ID for job in applied_jobs]
        }
    })