from sqlalchemy_define import db
from flask import request, jsonify
from models.job_application import JobApplication


def apply_for_job():
    data = request.get_json()
    jobID = data['JobList_ID']
    staffID = data['Staff_ID']
    job_application = JobApplication(JobList_ID=jobID, Staff_ID=staffID)

    try:
        db.session.add(job_application)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"An error occurred while applying for the job. Error: {str(e)}"}), 500

    return jsonify(job_application.json()), 201
