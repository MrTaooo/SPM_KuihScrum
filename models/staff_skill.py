from sqlalchemy_define import db

class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'

    Staff_ID = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'), primary_key=True)
    Skill_Name = db.Column(db.Text, db.ForeignKey('Role_Skill.Skill_Name'), nullable=False, primary_key=True)

    def __init__(self, Staff_ID, Skill_Name):
        self.Staff_ID = Staff_ID
        self.Skill_Name = Skill_Name

    def json(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Skill_Name": self.Skill_Name
        }