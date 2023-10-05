from sqlalchemy import *
from sqlalchemy_define import db

class AccessRights(db.Model):
    __tablename__ = 'AccessRights'

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_type = db.Column(db.String(50), nullable=False)

    def __init__(self, Access_ID, Access_type):
        self.Access_ID = Access_ID
        self.Access_type = Access_type
    
    def json(self):
        return {
            "Access_ID": self.Access_ID,
            "Access_type": self.Access_type
        }
    