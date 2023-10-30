from sqlalchemy_define import db

class AccessRights(db.Model):
    __tablename__ = 'AccessRights'

    Access_ID = db.Column(db.Integer, primary_key=True)
    Access_Control_Name = db.Column(db.String(50), nullable=False)

    def __init__(self, access_id, access_control_name):
        self.Access_ID = access_id
        self.Access_Control_Name = access_control_name
    
    def json(self):
        return {
            "Access_ID": self.Access_ID,
            "Access_Control_Name": self.Access_Control_Name
        }
    