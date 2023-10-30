from sqlalchemy_define import db

class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'), primary_key=True)
    Skill_Name = db.Column(db.Text, db.ForeignKey('Role_Skill.Skill_Name'), nullable=False, primary_key=True)

    def __init__(self, staff_id, skill_name):
        self.Staff_ID = staff_id
        self.Skill_Name = skill_name

    def json(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Skill_Name": self.Skill_Name
        }