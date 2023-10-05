from sqlalchemy_define import db
from sqlalchemy.dialects.mysql import LONGTEXT


class Role(db.Model):
    __tablename__ = 'Role'

    Role_Name = db.Column(db.String(20), primary_key=True)
    Role_Desc = db.Column(LONGTEXT, nullable=False)

    def __init__(self, Role_Name, Role_Desc):
        self.Role_Name = Role_Name
        self.Role_Desc = Role_Desc

    def json(self):
        return {
            "Role_Name": self.Role_Name,
            "Role_Desc": self.Role_Desc
        }