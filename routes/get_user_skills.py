from flask import request, jsonify
from sqlalchemy import *
from models.staff_skill import StaffSkill


# Get all skills for the 'logged in' user
def get_user_skills():
    # retrieve all user's skills from the database
    userID = request.args.get('userID')
    user_skills = StaffSkill.query.filter(StaffSkill.Staff_ID == userID).all()
    user_skills_list = []

    for user_skill in user_skills:
        skill_names = user_skill.Skill_Name
        # Append each skill individually
        user_skills_list.append(skill_names)
    return jsonify({
        "code": 200, 
        "data": {"user_skills": user_skills_list}
    })

    # no 404 return because there will always be skills for each user 