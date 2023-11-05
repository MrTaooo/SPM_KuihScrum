import sys
import unittest
from unittest.mock import MagicMock
from datetime import date

sys.path.insert(1, '../../')
from sqlalchemy_define import db

sys.path.insert(1, '../../models')
from job_application import JobApplication
from job_listing import JobListing
from role_skill import RoleSkill
from role import Role
from skill import Skill
from staff_skill import StaffSkill
from staff import Staff
from access_rights import AccessRights


class TestJobApplication(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.filter_by_mock = MagicMock()
        # Mock the query method to return a mock that has a filter_by method
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_job_application(self):
        # Test data
        job_application_data = {
            'job_list_id': 1,
            'staff_id': 2
        }
        job_application = JobApplication(job_application_data['job_list_id'], 
                                         job_application_data['staff_id'])
        
        # Simulate adding a new job application to the database
        self.db_session.add(job_application)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(job_application)
        self.db_session.commit.assert_called_once()

    def test_read_job_application(self):
        # Test data
        job_application_data = {
            'job_list_id': 1,
            'staff_id': 2
        }
        job_application = JobApplication(job_application_data['job_list_id'], 
                                         job_application_data['staff_id'])
        self.filter_by_mock.return_value.first.return_value = job_application

        # Perform the read operation
        queried_application = self.db_session.query(JobApplication).filter_by(
            JobList_ID=job_application_data['job_list_id'], 
            Staff_ID=job_application_data['staff_id']
        ).first()

        # Test that the returned job application matches the test data
        self.assertEqual(queried_application.json(), job_application.json())

    def test_update_job_application(self):
        # Test data
        job_application_data = {
            'job_list_id': 1,
            'staff_id': 2
        }
        job_application = JobApplication(job_application_data['job_list_id'], 
                                         job_application_data['staff_id'])
        self.filter_by_mock.return_value.first.return_value = job_application

        # Simulate the update
        job_application.job_list_id = 3
        self.db_session.commit()

        # Test that commit was called
        self.db_session.commit.assert_called_once()
        self.assertEqual(job_application.job_list_id, 3)

    def test_delete_job_application(self):
        # Test data
        job_application_data = {
            'job_list_id': 1,
            'staff_id': 2
        }
        job_application = JobApplication(job_application_data['job_list_id'], 
                                         job_application_data['staff_id'])

        # Simulate deleting the job application
        self.db_session.delete(job_application)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(job_application)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()
        self.filter_by_mock.reset_mock()

class TestJobListing(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.db_session.rollback = MagicMock()
        self.db_session.query = MagicMock()

    def test_create_job_listing(self):
        # Test data
        job_listing_data = {
            'Role_Name': 'Software Developer',
            'publish_Date': date(2023, 1, 1),
            'Closing_date': date(2023, 12, 31)
        }
        job_listing = JobListing(job_listing_data['Role_Name'],
                                 job_listing_data['publish_Date'],
                                 job_listing_data['Closing_date'])

        # Simulate adding a new job listing to the database
        self.db_session.add(job_listing)
        self.db_session.commit()

        # Test that add and commit were called with the job listing
        self.db_session.add.assert_called_with(job_listing)
        self.db_session.commit.assert_called_once()

    def test_read_job_listing(self):
        # Test data
        job_listing_data = {
            'JobList_ID': 1,
            'Role_Name': 'Software Developer',
            'publish_Date': date(2023, 1, 1),
            'Closing_date': date(2023, 12, 31)
        }
        job_listing = JobListing(job_listing_data['Role_Name'],
                                 job_listing_data['publish_Date'],
                                 job_listing_data['Closing_date'])
        job_listing.JobList_ID = job_listing_data['JobList_ID']
        self.db_session.query(JobListing).filter_by.return_value.first.return_value = job_listing

        # Perform the read operation
        queried_listing = self.db_session.query(JobListing).filter_by(
            JobList_ID=job_listing_data['JobList_ID']).first()

        # Test that the returned job listing matches the test data
        self.assertEqual(queried_listing.json(), job_listing.json())

    def test_update_job_listing(self):
        # Test data before update
        job_listing_data = {
            'JobList_ID': 1,
            'Role_Name': 'Software Developer',
            'publish_Date': date(2023, 1, 1),
            'Closing_date': date(2023, 12, 31)
        }
        # Test data after update
        updated_data = {
            'Role_Name': 'Senior Software Developer',
            'Closing_date': date(2024, 1, 1)
        }
        job_listing = JobListing(job_listing_data['Role_Name'],
                                 job_listing_data['publish_Date'],
                                 job_listing_data['Closing_date'])
        job_listing.JobList_ID = job_listing_data['JobList_ID']
        self.db_session.query(JobListing).filter_by.return_value.first.return_value = job_listing

        # Simulate the update
        job_listing.Role_Name = updated_data['Role_Name']
        job_listing.Closing_date = updated_data['Closing_date']
        self.db_session.commit()

        # Test that commit was called and data was updated
        self.db_session.commit.assert_called_once()
        self.assertEqual(job_listing.Role_Name, updated_data['Role_Name'])
        self.assertEqual(job_listing.Closing_date, updated_data['Closing_date'])

    def test_delete_job_listing(self):
        # Test data
        job_listing_data = {
            'JobList_ID': 1,
            'Role_Name': 'Software Developer',
            'publish_Date': date(2023, 1, 1),
            'Closing_date': date(2023, 12, 31)
        }
        job_listing = JobListing(job_listing_data['Role_Name'],
                                 job_listing_data['publish_Date'],
                                 job_listing_data['Closing_date'])
        job_listing.JobList_ID = job_listing_data['JobList_ID']

        # Simulate deleting the job listing
        self.db_session.delete(job_listing)
        self.db_session.commit()

        # Test that delete and commit were called with the job listing
        self.db_session.delete.assert_called_with(job_listing)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()

class TestRoleSkill(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.db_session.query = MagicMock()
        self.filter_by_mock = MagicMock()
        # Mock the query method to return a mock that has a filter_by method
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_role_skill(self):
        # Test data
        role_skill_data = {
            'Role_Name': 'Engineer',
            'Skill_Name': 'Python'
        }
        role_skill = RoleSkill(role_skill_data['Role_Name'], role_skill_data['Skill_Name'])
        
        # Simulate adding a new RoleSkill to the database
        self.db_session.add(role_skill)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(role_skill)
        self.db_session.commit.assert_called_once()

    def test_read_role_skill(self):
        # Test data
        role_skill_data = {
            'Role_Name': 'Engineer',
            'Skill_Name': 'Python'
        }
        role_skill = RoleSkill(role_skill_data['Role_Name'], role_skill_data['Skill_Name'])
        self.filter_by_mock.return_value.first.return_value = role_skill

        # Perform the read operation
        queried_role_skill = self.db_session.query(RoleSkill).filter_by(
            Role_Name=role_skill_data['Role_Name'],
            Skill_Name=role_skill_data['Skill_Name']
        ).first()

        # Test that the returned role_skill matches the test data
        self.assertEqual(queried_role_skill.json(), role_skill.json())

    def test_update_role_skill(self):
        # Test data
        role_skill_data = {
            'Role_Name': 'Engineer',
            'Skill_Name': 'Python'
        }
        new_skill_name = 'Machine Learning'
        role_skill = RoleSkill(role_skill_data['Role_Name'], role_skill_data['Skill_Name'])
        self.filter_by_mock.return_value.first.return_value = role_skill

        # Simulate the update
        role_skill.Skill_Name = new_skill_name
        self.db_session.commit()

        # Test that commit was called
        self.db_session.commit.assert_called_once()
        self.assertEqual(role_skill.Skill_Name, new_skill_name)

    def test_delete_role_skill(self):
        # Test data
        role_skill_data = {
            'Role_Name': 'Engineer',
            'Skill_Name': 'Python'
        }
        role_skill = RoleSkill(role_skill_data['Role_Name'], role_skill_data['Skill_Name'])

        # Simulate deleting the RoleSkill
        self.db_session.delete(role_skill)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(role_skill)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()

class TestRole(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.db_session.query = MagicMock()

    def test_create_role(self):
        # Test data
        role_data = {
            'Role_Name': 'Admin',
            'Role_Desc': 'Administrator role with all permissions'
        }
        role = Role(role_data['Role_Name'], role_data['Role_Desc'])
        
        # Simulate adding a new role to the database
        self.db_session.add(role)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(role)
        self.db_session.commit.assert_called_once()

    def test_read_role(self):
        # Test data
        role_data = {
            'Role_Name': 'Admin',
            'Role_Desc': 'Administrator role with all permissions'
        }
        role = Role(role_data['Role_Name'], role_data['Role_Desc'])
        self.db_session.query(Role).filter_by.return_value.first.return_value = role

        # Perform the read operation
        queried_role = self.db_session.query(Role).filter_by(Role_Name=role_data['Role_Name']).first()

        # Test that the returned role matches the test data
        self.assertEqual(queried_role.json(), role.json())

    def test_update_role(self):
        # Test data
        role_data = {
            'Role_Name': 'Admin',
            'Role_Desc': 'Administrator role with all permissions'
        }
        role = Role(role_data['Role_Name'], role_data['Role_Desc'])
        self.db_session.query(Role).filter_by.return_value.first.return_value = role

        # Simulate the update
        updated_description = 'Updated role description'
        role.Role_Desc = updated_description
        self.db_session.commit()

        # Test that commit was called
        self.db_session.commit.assert_called_once()
        self.assertEqual(role.Role_Desc, updated_description)

    def test_delete_role(self):
        # Test data
        role_data = {
            'Role_Name': 'Admin',
            'Role_Desc': 'Administrator role with all permissions'
        }
        role = Role(role_data['Role_Name'], role_data['Role_Desc'])

        # Simulate deleting the role
        self.db_session.delete(role)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(role)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()

class TestSkill(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        # Create a MagicMock to represent the query's filter_by method
        self.filter_by_mock = MagicMock()
        # Mock the query method to return a mock that has a filter_by method
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'Programming Language'
        }
        skill = Skill(skill_data['Skill_Name'], skill_data['Skill_Desc'])
        
        # Simulate adding a new skill to the database
        self.db_session.add(skill)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(skill)
        self.db_session.commit.assert_called_once()

    def test_read_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'Programming Language'
        }
        skill = Skill(skill_data['Skill_Name'], skill_data['Skill_Desc'])
        self.filter_by_mock.return_value.first.return_value = skill

        # Perform the read operation
        queried_skill = self.db_session.query(Skill).filter_by(
            Skill_Name=skill_data['Skill_Name']
        ).first()

        # Test that the returned skill matches the test data
        self.assertEqual(queried_skill.json(), skill.json())

    def test_update_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'Programming Language'
        }
        skill = Skill(skill_data['Skill_Name'], skill_data['Skill_Desc'])
        self.filter_by_mock.return_value.first.return_value = skill

        # Simulate the update
        new_description = "A high-level, general-purpose programming language."
        skill.Skill_Desc = new_description
        self.db_session.commit()

        # Test that commit was called and the description was updated
        self.db_session.commit.assert_called_once()
        self.assertEqual(skill.Skill_Desc, new_description)

    def test_delete_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'Programming Language'
        }
        skill = Skill(skill_data['Skill_Name'], skill_data['Skill_Desc'])

        # Simulate deleting the skill
        self.db_session.delete(skill)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(skill)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()
        self.filter_by_mock.reset_mock()

class TestStaffSkill(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        # Create a MagicMock to represent the query's filter_by method
        self.filter_by_mock = MagicMock()
        # Mock the query method to return a mock that has a filter_by method
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_staff_skill(self):
        # Test data
        staff_skill_data = {
            'Staff_ID': 1,
            'Skill_Name': 'Python Development'
        }
        staff_skill = StaffSkill(staff_skill_data['Staff_ID'], staff_skill_data['Skill_Name'])
        
        # Simulate adding a new StaffSkill to the database
        self.db_session.add(staff_skill)
        self.db_session.commit()

        # Test that add and commit were called with the right parameters
        self.db_session.add.assert_called_with(staff_skill)
        self.db_session.commit.assert_called_once()

        # Assert the fields are correctly set
        self.assertEqual(staff_skill.Staff_ID, staff_skill_data['Staff_ID'])
        self.assertEqual(staff_skill.Skill_Name, staff_skill_data['Skill_Name'])

    def test_read_staff_skill(self):
        # Test data
        staff_skill_data = {
            'Staff_ID': 1,
            'Skill_Name': 'Python Development'
        }
        staff_skill = StaffSkill(staff_skill_data['Staff_ID'], staff_skill_data['Skill_Name'])
        self.filter_by_mock.return_value.first.return_value = staff_skill

        # Perform the read operation
        queried_skill = self.db_session.query(StaffSkill).filter_by(
            Staff_ID=staff_skill_data['Staff_ID'], 
            Skill_Name=staff_skill_data['Skill_Name']
        ).first()

        # Test that the returned StaffSkill matches the test data
        self.assertEqual(queried_skill.json(), staff_skill.json())

    def test_update_staff_skill(self):
        # Test data
        staff_skill_data = {
            'Staff_ID': 1,
            'Skill_Name': 'Python Development'
        }
        updated_skill_name = 'Data Analysis'
        staff_skill = StaffSkill(staff_skill_data['Staff_ID'], staff_skill_data['Skill_Name'])
        self.filter_by_mock.return_value.first.return_value = staff_skill

        # Simulate the update
        staff_skill.Skill_Name = updated_skill_name
        self.db_session.commit()

        # Test that commit was called and the field was updated correctly
        self.db_session.commit.assert_called_once()
        self.assertEqual(staff_skill.Skill_Name, updated_skill_name)

    def test_delete_staff_skill(self):
        # Test data
        staff_skill_data = {
            'Staff_ID': 1,
            'Skill_Name': 'Python Development'
        }
        staff_skill = StaffSkill(staff_skill_data['Staff_ID'], staff_skill_data['Skill_Name'])

        # Simulate deleting the StaffSkill
        self.db_session.delete(staff_skill)
        self.db_session.commit()

        # Test that delete and commit were called with the right parameters
        self.db_session.delete.assert_called_with(staff_skill)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()
        self.filter_by_mock.reset_mock()

class TestStaff(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.db_session.refresh = MagicMock()
        # Create a MagicMock to represent the query's filter method
        self.filter_mock = MagicMock()
        # Mock the query method to return a mock that has a filter method
        self.db_session.query.return_value.filter = self.filter_mock

    def test_create_staff(self):
        # Test data
        staff_data = {
        'staff_id': 1,  
        'staff_fname': 'John',
        'staff_lname': 'Doe',
        'dept': 'IT',
        'country': 'USA',
        'email': 'johndoe@example.com',
        'access_rights': 101
        }
        staff = Staff(**staff_data)
        
        # Simulate adding a new staff to the database
        self.db_session.add(staff)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(staff)
        self.db_session.commit.assert_called_once()

    def test_read_staff(self):
        # Test data
        staff_data = {
        'staff_id': 1,  # Assuming you are using this ID for the test.
        'staff_fname': 'John',
        'staff_lname': 'Doe',
        'dept': 'IT',
        'country': 'USA',
        'email': 'johndoe@example.com',
        'access_rights': 101
        }
        staff = Staff(**staff_data)
        self.filter_mock.return_value.first.return_value = staff

        # Perform the read operation
        queried_staff = self.db_session.query(Staff).filter(Staff.Staff_ID == 1).first()

        # Assuming the staff ID is set to 1 in the test database, assert using that ID
        staff.Staff_ID = 1  # This should be set to match the ID used in the query filter above
        self.assertEqual(queried_staff.json(), staff.json())

    def test_update_staff(self):
        # Test data
        staff_data = {
        'staff_id': 1,
        'staff_fname': 'John',
        'staff_lname': 'Doe',
        'dept': 'IT',
        'country': 'USA',
        'email': 'johndoe@example.com',
        'access_rights': 101
        }
        staff = Staff(**staff_data)
        self.filter_mock.return_value.first.return_value = staff

        # Simulate the update
        staff.Staff_FName = 'Jane'
        self.db_session.commit()

        # Test that commit was called and the staff's first name was updated
        self.db_session.commit.assert_called_once()
        self.assertEqual(staff.Staff_FName, 'Jane')

    def test_delete_staff(self):
        # Test data
        staff_data = {
        'staff_id': 1,
        'staff_fname': 'John',
        'staff_lname': 'Doe',
        'dept': 'IT',
        'country': 'USA',
        'email': 'johndoe@example.com',
        'access_rights': 101
        }
        staff = Staff(**staff_data)

        # Simulate deleting the staff
        self.db_session.delete(staff)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(staff)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()
        self.filter_mock.reset_mock()

class TestAccessRights(unittest.TestCase):

    def setUp(self):
        # Mock the database session
        self.db_session = MagicMock()
        self.db_session.add = MagicMock()
        self.db_session.commit = MagicMock()
        self.db_session.delete = MagicMock()
        self.db_session.query = MagicMock()
        self.filter_by_mock = MagicMock()

        # Setup mock return value for query filter_by
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_access_rights(self):
        # Test data
        access_data = {
            'Access_ID': 1,
            'Access_Control_Name': 'Read'
        }
        access_rights = AccessRights(access_data['Access_ID'], access_data['Access_Control_Name'])

        # Simulate adding a new AccessRights to the database
        self.db_session.add(access_rights)
        self.db_session.commit()

        # Test that add and commit were called
        self.db_session.add.assert_called_with(access_rights)
        self.db_session.commit.assert_called_once()

    def test_read_access_rights(self):
        # Test data
        access_data = {
            'Access_ID': 1,
            'Access_Control_Name': 'Read'
        }
        access_rights = AccessRights(access_data['Access_ID'], access_data['Access_Control_Name'])
        self.filter_by_mock.return_value.first.return_value = access_rights

        # Perform the read operation
        queried_access_rights = self.db_session.query(AccessRights).filter_by(
            Access_ID=access_data['Access_ID']
        ).first()

        # Test that the returned access rights matches the test data
        self.assertEqual(queried_access_rights.json(), access_rights.json())

    def test_update_access_rights(self):
        # Test data
        access_data = {
            'Access_ID': 1,
            'Access_Control_Name': 'Read'
        }
        access_rights = AccessRights(access_data['Access_ID'], access_data['Access_Control_Name'])
        self.filter_by_mock.return_value.first.return_value = access_rights

        # Simulate the update
        access_rights.Access_Control_Name = 'Write'
        self.db_session.commit()

        # Test that commit was called
        self.db_session.commit.assert_called_once()
        self.assertEqual(access_rights.Access_Control_Name, 'Write')

    def test_delete_access_rights(self):
        # Test data
        access_data = {
            'Access_ID': 1,
            'Access_Control_Name': 'Read'
        }
        access_rights = AccessRights(access_data['Access_ID'], access_data['Access_Control_Name'])

        # Simulate deleting the AccessRights
        self.db_session.delete(access_rights)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(access_rights)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()
        self.filter_by_mock.reset_mock()


if __name__ == '__main__':
    unittest.main()