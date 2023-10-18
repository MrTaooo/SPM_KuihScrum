from flask import request, jsonify
from models.job_listing import JobListing  
from sqlalchemy_define import db
from datetime import datetime

def edit_listing():
    data = request.get_json()
    print(data)
    listing_id = data["id"]
    new_closingDate = data["closingDate"]
    roleName = data["roleName"]
    current_date = datetime.now().strftime("%Y-%m-%d")

    # check if the new closing date is empty
    if not new_closingDate:
        return jsonify({
            "code": 409,
            "message": "Please select a date!"
        })
    
     # retrieve duplicate role listing (exact role name, publish date is before closing date, closing date is after today)
    overlapping_listings = db.session.query(JobListing).filter(
        JobListing.Role_Name == roleName,
        JobListing.publish_Date <= new_closingDate,
        JobListing.Closing_date >= current_date,
        JobListing.JobList_ID != listing_id
    ).all()
    print(overlapping_listings)
    
    # Check if the role listing for the role exists in the database
    if overlapping_listings:
        return jsonify({
            "code": 409,
            "message": "Error, cannot have duplicate listings!"
        })
    
    if new_closingDate < current_date:
        return jsonify({
            "code": 409,
            "message": "Error, cannot select closing date that is before today!"
        })
    if new_closingDate == current_date:
        return jsonify({
            "code": 409,
            "message": "Error, cannot select closing date that is on the same day!"
        })

    listing = db.session.query(JobListing).filter(JobListing.JobList_ID == listing_id).first()
    if not listing:
        return jsonify({
            "code": 404,
            "message": "Error, listing not found!"
        })
    
    
    
    
   
    listing.Closing_date = new_closingDate
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "Listing updated successfully!"
    })

    