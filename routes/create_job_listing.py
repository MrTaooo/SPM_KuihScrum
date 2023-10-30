from flask import request, jsonify
from sqlalchemy import *
from flask import jsonify
from models.job_listing import JobListing
from sqlalchemy_define import db
from datetime import datetime

# Process job listing creation


def create_listing():
    # using Flask's request object to extract JSON data from the HTTP request sent by a client.
    data = request.get_json()
    roleTitle = data["roleTitle"]
    closingDate = data["closingDate"]
    print(closingDate)
    date = datetime.now()
    strdate = date.strftime("%Y-%m-%d")
    # print(closingDate)

    # check if the closing date is empty
    if (closingDate == ''):
        return jsonify({
            "code": 409,
            "message": "Please select a date!"
        })
    
    # retrieve duplicate role listing (exact role name, publish date is before closing date, closing date is after today)
    overlapping_listings = db.session.query(JobListing).filter(
        JobListing.Role_Name == roleTitle,
        JobListing.publish_Date <= closingDate,
        JobListing.Closing_date >= date
    ).all()
    
    # Check if the role listing for the role exists in the database
    if overlapping_listings:
        return jsonify({
            "code": 409,
            "message": "Error, cannot have duplicate listings!"
        })

    if (closingDate < strdate):
        return jsonify({
            "code": 409,
            "message": "Error, cannot select closing date that is before today!"
        })
    if (closingDate == strdate):
        return jsonify({
            "code": 409,
            "message": "Error, cannot select closing date that is on the same day!"
        })

    

    # If no duplicate listing found, save the new listing to the database
    new_listing = JobListing(
        role_name=roleTitle, publish_date=date, closing_date=closingDate)
    db.session.add(new_listing)
    db.session.commit()

    # Return a response, for example, a confirmation message
    return jsonify({
        "code": 201,
        "message": "Data received and processed successfully!"
    })
