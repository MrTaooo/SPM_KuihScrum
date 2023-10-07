from sqlalchemy_define import db
from flask import request, jsonify
from models.job_application import JobApplication

def withdraw_application():
    # using Flask's request object to extract JSON data from the HTTP request sent by a client.
    data = request.get_json()

    # retrieve all the job applications for the staff
    job_application = JobApplication.query.filter_by(
        JobList_ID=data['JobList_ID'], Staff_ID=data['Staff_ID']).first()

    if job_application:
        db.session.delete(job_application)
        db.session.commit()
        return jsonify({
            "code":200, 
            "message": "Successfully withdrew the application."
        })
    return jsonify({
        "code":404,
        "message": "Application not found."
    })