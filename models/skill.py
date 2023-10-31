from sqlalchemy_define import db
class Skill(db.Model):
    __tablename__ = 'Skill'

    Skill_Name = db.Column("Skill_Name", primary_key=True)
    Skill_Desc = db.Column("Skill_Desc", nullable=False)

    def __init__(self, skill_name, skill_desc):
        self.Skill_Name = skill_name
        self.Skill_Desc = skill_desc

    def json(self):
        return {
            "Skill_Name": self.Skill_Name,
            "Skill_Desc": self.Skill_Desc
        }