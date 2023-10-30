from sqlalchemy_define import db

class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'

    Role_Name = db.Column(db.String(20), db.ForeignKey(
        'Role.Role_Name'), primary_key=True)
    Skill_Name = db.Column(db.Text, nullable=False, primary_key=True)

    def __init__(self, role_name, skill_name):
        self.Role_Name = role_name
        self.Skill_Name = skill_name

    def json(self):
        return {
            "Role_Name": self.Role_Name,
            "Skill_Name": self.Skill_Name
        }