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

    def __init__(self, staff_id, staff_fname, staff_lname, dept, country, email, access_rights):
        self.Staff_ID = staff_id
        self.Staff_FName = staff_fname
        self.Staff_LName = staff_lname
        self.Dept = dept
        self.Country = country
        self.Email = email
        self.Access_Rights = access_rights

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