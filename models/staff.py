from sqlalchemy_define import db

class Staff(db.Model):
    __tablename__ = 'Staff'

    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.Text, nullable=False)
    Staff_LName = db.Column(db.Text, nullable=False)
    Dept = db.Column(db.Text, nullable=False)
    Country = db.Column(db.Text, nullable=False)
    Email = db.Column(db.Text, nullable=False)
    Access_Rights = db.Column(db.Integer, db.ForeignKey('AccessRights.Access_ID'))

    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Dept, Country, Email, Access_Rights):
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Country = Country
        self.Email = Email
        self.Access_Rights = Access_Rights

    def json(self):
        return {
            "Staff_ID": self.Staff_ID,
            "Staff_FName": self.Staff_FName,
            "Staff_LName": self.Staff_LName,
            "Dept": self.Dept,
            "Country": self.Country,
            "Email": self.Email,
            "Access_Rights": self.Access_Rights
        }