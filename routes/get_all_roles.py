from flask import jsonify
from models.role import Role  # Import the Role model if needed

def get_all_roles():
    # retrieve all the roles from the database
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