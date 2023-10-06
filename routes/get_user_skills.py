from flask import request, jsonify
from sqlalchemy import *
from models.staff_skill import StaffSkill


# Get all skills for the 'logged in' user
def get_user_skills():
    # retrieve all user's skills from the database
    userID = request.args.get('userID')
    user_skills = StaffSkill.query.filter(StaffSkill.Staff_ID == userID).all()
    user_skill_dict = {}
    user_skill_dict[userID] = []

    for user_skill in user_skills:
        skill_names = user_skill.Skill_Name
        # Append each skill individually
        user_skill_dict[userID].append(skill_names)

    print(user_skill_dict)
    return jsonify({
        "code": 200, 
        "data": {"user_skills": [user_skill_dict]}
    })

    # no 404 return because there will always be skills for each user 