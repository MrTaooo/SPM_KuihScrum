from flask import jsonify
from models.role_skill import RoleSkill  # Import the Role model if needed

# Get all related skills for each role
def get_roles_skills():
    # retrieve all role skills from the database
    role_skills = RoleSkill.query.all()
    role_skill_dict = {}

    for role_skill in role_skills:
        role_name = role_skill.Role_Name
        skill_name = role_skill.Skill_Name #removed .split(', ') since the skills are individually listed
        if role_name not in role_skill_dict:
            role_skill_dict[role_name] = []

        # Append each skill individually
        role_skill_dict[role_name].append(skill_name)

    # Join the skills into a comma-separated string
    # role_skill_dict = {role: ', '.join(skills)
    #                    for role, skills in role_skill_dict.items()}

    return jsonify({
        "code": 200, 
        "data": {"roles_skills": [role_skill_dict]}
    })

    # no 404 return because there will always be skills for each role 