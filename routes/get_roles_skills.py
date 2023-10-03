from flask import jsonify
from models.role_skill import RoleSkill  # Import the Role model if needed

# Get all related skills for each role
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
    role_skill_dict = {role: ', '.join(skills)
                       for role, skills in role_skill_dict.items()}
    
    return {"code": 200, "data": {"roles_skills": [role_skill_dict]}}