from flask import request, jsonify
from sqlalchemy import *
from models.job_listing import JobListing 
from models.role_skill import RoleSkill 
from models.staff_skill import StaffSkill
from sqlalchemy_define import db

def calculate_alignment():
    # using Flask's request object to extract JSON data from the HTTP request sent by a client.
    data = request.get_json()
    userID = data['user_ID']
    joblist_ID = data['joblist_ID']
 
    # retrieve the job_listing from the database based on jobList_ID
    job_listing = JobListing.query.filter_by(JobList_ID=joblist_ID).first() 
    
    if job_listing is None:
        return jsonify({"code": 404, "message": "Job listing not found"})
    
    role_name = job_listing.Role_Name
    # retriieve the role skills for the role of the job listing
    role_skills = db.session.query(RoleSkill).filter(RoleSkill.Role_Name==role_name).all()
    
    if not role_skills:
        return jsonify({"code":404, "message": "Skills for the role not found"})

    # skills_by_role = {}
    skills_by_role = []
    
    for skill_record in role_skills:
        # role = skill_record.Role_Name
        skill = skill_record.Skill_Name

        skills_by_role.append(skill)

    # print("Skills by Role:", skills_by_role)
    
    # retrieve the staff skill based on staff id
    user_skills = StaffSkill.query.filter(StaffSkill.Staff_ID == userID).all()
    
    user_skills_dict = {}
    
    for user_record in user_skills:
        skill = user_record.Skill_Name
        
        # Add the skill to the list of skills for the user
        user_skills_dict.setdefault("user_skills", []).append(skill)

    # Extract user skills
    user_skills_count = user_skills_dict.get("user_skills", []) 
    # Extract role-specific skills 
    role_skills_count = skills_by_role
    # Find the number of skills that are aligned between the user and the role
    aligned_skills = len(set(user_skills_count).intersection(role_skills_count))
    # Calculate the alignment percentage
    alignment_percentage = round((aligned_skills / len(role_skills_count)) * 100) if role_skills_count else 0.0
    
    return jsonify({
        "code": 200, 
        "data": {
            "alignment_percentage": alignment_percentage, 
            "user_skills_dict": user_skills_dict,  # This will contain all the user's skills
            "skills_by_role": skills_by_role,  # This will contain all skills related to the role 
        }
    })