from flask import jsonify
from sqlalchemy_define import db
from models.skill import Skill  # Import the Skill model

# Get all skills
def get_skills():
    # Retrieve all skills from the database
    skills = Skill.query.all()
    skill_list = []

    # Append each skill to the list
    for skill in skills:
        skill_list.append(skill.json())

    return jsonify({
        "code": 200, 
        "data": {"skills": skill_list}
    })
