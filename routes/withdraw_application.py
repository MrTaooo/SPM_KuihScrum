from sqlalchemy_define import db
from flask import request, jsonify
from models.job_application import JobApplication

def withdraw_application():
    data = request.get_json()
    job_application = JobApplication.query.filter_by(
        JobList_ID=data['JobList_ID'], Staff_ID=data['Staff_ID']).first()

    if job_application:
        db.session.delete(job_application)
        db.session.commit()
        return jsonify({"message": "Successfully withdrew the application."}), 200
    return jsonify({"message": "Application not found."}), 404