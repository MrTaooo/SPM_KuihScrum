from flask import request, jsonify
from models.job_listing import JobListing  
from sqlalchemy_define import db
from datetime import datetime

def edit_listing():
    data = request.get_json()
    listing_id = data["id"]
    new_closingDate = data["closingDate"]
    current_date = datetime.now().strftime("%Y-%m-%d")

    # check if the new closing date is empty
    if not new_closingDate:
        return jsonify({
            "code": 409,
            "message": "Please select a date"
        })
    
    if new_closingDate <= current_date:
        return jsonify({
            "code": 409,
            "message": "Error, cannot select closing date that is before today"
        })

    listing = db.session.query(JobListing).filter(JobListing.JobList_ID == listing_id).first()
    if not listing:
        return jsonify({
            "code": 404,
            "message": "Error, listing not found"
        })

    listing.Closing_date = new_closingDate
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "Listing updated successfully"
    })
