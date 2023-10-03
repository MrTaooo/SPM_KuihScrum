from flask import request, jsonify
from sqlalchemy import *
from flask import jsonify
from models.job_listing import JobListing  # Import the Role model if needed
from sqlalchemy_define import db
from datetime import datetime

# Process job listing creation
def create_listing():
    data = request.get_json()
    roleTitle = data["roleTitle"]
    closingDate = data["closingDate"]
    date = datetime.now()
    print(closingDate)
    if (closingDate == ''):
        return jsonify({
            "code": 409,
            "message": "Please select a date"
        })

    if (closingDate < str(date)):
        return jsonify({
            "code": 409,
            "message": "Error, closing date cannot be in the past"
        })

    # Check if the role listing for the role exists in the database
    overlapping_listings = db.session.query(JobListing).filter(
        JobListing.Role_Name == roleTitle,
        JobListing.publish_Date <= closingDate,
        JobListing.Closing_date >= date
    ).all()

    if overlapping_listings:
        return jsonify({
            "code": 409,
            "message": "Error, cannot have duplicate listings"
        })

    # If no duplicate listing found, save the new listing to the database
    new_listing = JobListing(
        Role_Name=roleTitle, publish_Date=date, Closing_date=closingDate)
    db.session.add(new_listing)
    db.session.commit()

    # Return a response, for example, a confirmation message
    return jsonify({
        "code": 201,
        "message": "Data received and processed successfully"
    })