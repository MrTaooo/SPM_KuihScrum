from flask import Flask
import os

# Import the create_app function from your module
from sqlalchemy_define import create_app

# Create the Flask app instance using the create_app function
app = create_app()

# Import and register the route functions from the route files
from routes.apply_for_job import apply_for_job
from routes.calculate_alignment import calculate_alignment
from routes.create_job_listing import create_listing
from routes.edit_job_listing import edit_listing
from routes.get_all_job_listings import get_all_joblistings
from routes.get_all_roles import get_all_roles
from routes.get_roles_skills import get_roles_skills
from routes.get_user_skills import get_user_skills
from routes.withdraw_application import withdraw_application
from routes.get_applied_jobs_for_user import get_applied_jobs_for_user
from routes.get_all_applicants import get_applicants

# Register the route functions with the app
app.route("/apply_for_job", methods=['POST'])(apply_for_job)
app.route('/calculateAlignment', methods=['GET'])(calculate_alignment)
app.route('/createListing', methods=['POST'])(create_listing)
app.route('/editListing', methods=['POST'])(edit_listing)
app.route("/joblistings")(get_all_joblistings)
app.route("/roles")(get_all_roles)
app.route("/rolesSkills")(get_roles_skills)
app.route("/userSkills")(get_user_skills)
app.route("/withdraw_application", methods=['POST'])(withdraw_application)
app.route("/get_applied_jobs_for_user/<int:staff_id>", methods=['GET'])(get_applied_jobs_for_user)
app.route("/get_all_applicants/<int:joblist_ID>", methods=['GET'])(get_applicants)


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
