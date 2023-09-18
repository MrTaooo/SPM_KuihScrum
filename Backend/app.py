from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

# -------------- Import for Notification Service (START) --------------
# import amqp_setup
# import pika
import json
# --------------- Import for Notification Service (End) ---------------

# -------------- Import for Job Listing /createlisting (START) --------------
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# -------------- Import for Job Listing /createlisting (END) --------------
app = Flask(__name__)
CORS(app)

# -------------- Connection to mySQL DB --------------
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/spm_kuih' # Replace with your MySQL credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/SPM_KUIH'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Class: Role
class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = db.Column(db.String(20), primary_key=True)
    Role_Desc = db.Column(db.Text, nullable=False)

    def __init__(self, Role_Name, Role_Desc):
        self.Role_Name = Role_Name
        self.Role_Desc = Role_Desc

    def json(self):
        return {
                "Role_Name": self.Role_Name, 
                "Role_Desc": self.Role_Desc
        }
    
# Model Class: Job_Listing
class JobListing(db.Model):
    __tablename__ = 'Job_Listing'

    JobList_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_Name = db.Column(db.String(50), db.ForeignKey('Role.Role_Name'), nullable=False)
    publish_Date = db.Column(db.Date, nullable=False)
    Closing_date = db.Column(db.Date, nullable=False)

    def __init__(self, Role_Name, publish_Date, Closing_date):
        self.Role_Name = Role_Name
        self.publish_Date = publish_Date
        self.Closing_date = Closing_date

    def json(self):
        return {
            "JobList_ID": self.JobList_ID,
            "Role_Name": self.Role_Name,
            "publish_Date": self.publish_Date.strftime('%Y-%m-%d'),
            "Closing_date": self.Closing_date.strftime('%Y-%m-%d')
        }


#Get all roles in company
@app.route("/roles")
def get_all_roles():
    rolelist = Role.query.all()
    if len(rolelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in rolelist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no roles available."
        }
    ), 404

#Get all Job Listings
@app.route("/joblistings")
def get_all_joblistings():
    joblistings = JobListing.query.all()
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
            "message": "There are no job listings that are currently open."
        }
    ), 404





@app.route("/apply_role", methods=['POST'])
def apply_role():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            applicantDetails = request.get_json()
            print("\nReceived an applicationDetails in JSON:", applicantDetails)

            # do the actual work
            # 1. Send applicationDetails
            result = processApplication(applicantDetails)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "app.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400



# Process job listing creation 
@app.route('/createlisting', methods=['POST'])
def createlisting():
    data = request.get_json()
    roletitle = data["roletitle"] 
    closingdate = data["closingdate"]
    date = datetime.now()
    if (closingdate < date): 
        return "Error, closing date cannot be the day before "
    # Check for duplicate job listings using a raw SQL query
    query = "SELECT * FROM job_listings WHERE roletitle = %s AND closingdate = %s"
    result = db.engine.execute(query, (roletitle, closingdate)).fetchone()

    if result:
        return "Error, cannot have duplicate listings"

      # If no duplicate listing is found, insert the new job listing
    insert_query = "INSERT INTO job_listings (roletitle, publish_date, closingdate) VALUES (%s, %s, %s)"
    db.engine.execute(insert_query, (roletitle, date, closingdate))

    # Return a response, for example, a confirmation message
    return jsonify({"message": "Data received and processed successfully"})
   

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for All-in-one Skill-based Role Portal (SBRP)")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
