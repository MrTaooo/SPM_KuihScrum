from flask import request, jsonify
from sqlalchemy import *
from models.job_listing import JobListing 
from models.role_skill import RoleSkill 
from models.staff_skill import StaffSkill
from sqlalchemy_define import db

def calculate_alignment():
    
    user_skills = request.args.get('user_Skills').split(',')
    joblist_ID = request.args.get('joblist_ID')
 
    # retrieve the job_listing from the database based on jobList_ID
    job_listing = JobListing.query.filter_by(JobList_ID=joblist_ID).first() 
    
    if job_listing is None:
        return jsonify({"code": 404, "message": "Job listing not found"})
    
    role_name = job_listing.Role_Name
    # retriieve the role skills for the role of the job listing
    role_skills = db.session.query(RoleSkill).filter(RoleSkill.Role_Name==role_name).all()
    
    if not role_skills:
        return jsonify({"code":404, "message": "Skills for the role not found"})

    skills_by_role = []
    
    for skill_record in role_skills:
        # role = skill_record.Role_Name
        skill = skill_record.Skill_Name
        skills_by_role.append(skill)

    # Find the number of skills that are aligned between the user and the role
    aligned_skills = len(set(user_skills).intersection(skills_by_role))
    # Calculate the alignment percentage
    alignment_percentage = round((aligned_skills / len(skills_by_role)) * 100) if skills_by_role else 0.0

    return jsonify({
        "code": 200, 
        "data": {
            "alignment_percentage": alignment_percentage,
            "skills_by_role": skills_by_role,  # This will contain all skills related to the role 
        }
    })