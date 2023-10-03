from sqlalchemy_define import db

class JobApplication(db.Model):
    __tablename__ = 'Job_Application'

    JobList_ID = db.Column(db.Integer, primary_key=True)
    Staff_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, JobList_ID, Staff_ID):
        self.JobList_ID = JobList_ID
        self.Staff_ID = Staff_ID

    def json(self):
        return {
            "JobList_ID": self.JobList_ID,
            "Staff_ID": self.Staff_ID
        }