from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_cors import CORS

import os
import sys
import platform

# -------------- Import for Job Listing /createListing (START) --------------
from datetime import datetime
# -------------- Import for Job Listing /createListing (END) --------------
app = Flask(__name__)
CORS(app)

# -------------- Connection to mySQL DB --------------
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/SPM_KUIH'  # FOR WINDOW
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/SPM_KUIH'  # FOR MAC

def check_os():
    system = platform.system()  # Get the name of the operating system
    print(system)
    if system == 'Windows':
        return 'mysql+mysqlconnector://root@localhost:3306/SPM_KUIH'  # For Windows
    elif system == 'Darwin':
        return 'mysql+mysqlconnector://root:root@localhost:3306/SPM_KUIH'  # For macOS
    else:
        raise ValueError("Unsupported operating system")

app.config['SQLALCHEMY_DATABASE_URI'] = check_os()  # Set the URI based on the OS
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
    Role_Name = db.Column(db.String(50), db.ForeignKey(
        'Role.Role_Name'), nullable=False)
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

# Model Class: RoleSkill
class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'

    Role_Name = db.Column(db.String(20), db.ForeignKey('Role.Role_Name'), primary_key=True)
    Skill_Name = db.Column(db.Text, nullable=False)

    def __init__(self, Role_Name, Skill_Name):
        self.Role_Name = Role_Name
        self.Skill_Name = Skill_Name

    def json(self):
        return {
            "Role_Name": self.Role_Name,
            "Skill_Name": self.Skill_Name
        }



# Get all roles in company
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


# Get all related skills for each role
@app.route("/rolesSkills")
def get_roles_skills():
    role_skills = RoleSkill.query.all()

    role_skill_dict = {}

    for role_skill in role_skills:
        role_name = role_skill.Role_Name
        skill_names = role_skill.Skill_Name.split(', ')

        if role_name not in role_skill_dict:
            role_skill_dict[role_name] = []

        # Append each skill individually
        role_skill_dict[role_name].extend(skill_names)

    # Join the skills back into a comma-separated string
    role_skill_dict = {role: ', '.join(skills) for role, skills in role_skill_dict.items()}

    return role_skill_dict



# Get all related skills for each job listing 
@app.route("/rolesDescription")
def get_roles_description(): 
    roles = Role.query.all()

    role_listings = [role.json() for role in roles]

    role_dict = {role["Role_Name"]: role["Role_Desc"] for role in role_listings}

    return role_dict


# Get all Job Listings
@app.route("/joblistings")
def get_all_joblistings():
    joblistings = JobListing.query.order_by(desc(JobListing.publish_Date)).all()
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


# Process job listing creation
@app.route('/createListing', methods=['POST'])
def createListing():
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
            "message": "Error, closing date cannot be the day before"
        })
    # Check for duplicate job listings using a raw SQL query
    #query = "SELECT * FROM job_listing WHERE Role_Name = %s AND Closing_date = %s"
    # result = JobListing.query.filter_by(
    #     Role_Name=roleTitle, Closing_date=closingDate).first()

    # if result:
    #     return jsonify({
    #         "code": 409,
    #         "message": "Error, cannot have duplicate listings"
    #     })

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


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for All-in-one Skill-based Role Portal (SBRP)")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
