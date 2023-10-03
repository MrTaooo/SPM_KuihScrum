from sqlalchemy_define import db

class JobListing(db.Model):
    __tablename__ = 'Job_Listing'

    JobList_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role_Name = db.Column(db.String(50), db.ForeignKey(
        'Role.Role_Name'), nullable=False)
    publish_Date = db.Column(db.Date, nullable=False)
    Closing_date = db.Column(db.Date, nullable=False)

    def __init__(self, Role_Name, publish_Date, Closing_date):
        self.Role_Name = Role_Name
        self.publish_Date = publish_Date
        self.Closing_date = Closing_date

    def json(self):
        return {
            "JobList_ID": self.JobList_ID,
            "Role_Name": self.Role_Name,
            "publish_Date": self.publish_Date.strftime('%Y-%m-%d'),
            "Closing_date": self.Closing_date.strftime('%Y-%m-%d')
        }