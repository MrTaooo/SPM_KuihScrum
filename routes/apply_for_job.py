from sqlalchemy_define import db
from flask import request, jsonify
from models.job_application import JobApplication

def apply_for_job():
    # using Flask's request object to extract JSON data from the HTTP request sent by a client.
    data = request.get_json()
    job_id = data['JobList_ID']
    staff_id = data['Staff_ID']
    # create a new job application object
    job_application = JobApplication(job_list_id=job_id, staff_id=staff_id)

    try:
        db.session.add(job_application)
        db.session.commit()
    except Exception:
        return jsonify({
            "code": 404,
            "message": "Job application has been applied previously."
        })

    return jsonify({
        "code": 200,
        "message": "Job application created successfully."
    })
