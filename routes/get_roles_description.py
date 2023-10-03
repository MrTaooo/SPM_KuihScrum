from flask import jsonify
from models.role import Role  # Import the Role model if needed


# Get all related skills for each job listing
def get_roles_description():
    roles = Role.query.all()

    role_listings = [role.json() for role in roles]

    role_dict = {role["Role_Name"]: role["Role_Desc"]
                 for role in role_listings}

    return role_dict