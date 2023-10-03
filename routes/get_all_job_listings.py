from flask import jsonify
from sqlalchemy import *
from models.job_listing import JobListing  # Import the Role model if needed
from sqlalchemy_define import db

# Get all Job Listings
def get_all_joblistings():
    joblistings = JobListing.query.order_by(
        desc(JobListing.publish_Date)).all()
    if len(joblistings):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "joblistings": [joblisting.json() for joblisting in joblistings]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no job listings in the database."
        }
    ), 404