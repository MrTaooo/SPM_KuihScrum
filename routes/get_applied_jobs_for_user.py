from sqlalchemy_define import db
from flask import request, jsonify
from models.job_application import JobApplication

def get_applied_jobs_for_user(staff_id):
    applied_jobs = JobApplication.query.filter_by(Staff_ID=staff_id).all()
    return jsonify(
        {"appliedJobs": [job.JobList_ID for job in applied_jobs]}
    ), 200
