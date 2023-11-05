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
        self.db_session.query = MagicMock()
        self.db_session.flush = MagicMock()

        # Create a MagicMock to represent the query's filter_by method
        self.filter_by_mock = MagicMock()
        
        # Mock the query method to return a mock that has a filter_by method
        self.db_session.query.return_value.filter_by = self.filter_by_mock

    def test_create_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'A high-level programming language.'
        }
        skill = Skill(skill_name=skill_data['Skill_Name'], skill_desc=skill_data['Skill_Desc'])
        
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
            'Skill_Desc': 'A high-level programming language.'
        }
        skill = Skill(skill_name=skill_data['Skill_Name'], skill_desc=skill_data['Skill_Desc'])
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
            'Skill_Desc': 'A high-level programming language.'
        }
        skill = Skill(skill_name=skill_data['Skill_Name'], skill_desc=skill_data['Skill_Desc'])
        self.filter_by_mock.return_value.first.return_value = skill

        # Simulate the update
        updated_desc = 'An interpreted language with dynamic semantics.'
        skill.Skill_Desc = updated_desc
        self.db_session.commit()

        # Test that commit was called
        self.db_session.commit.assert_called_once()
        self.assertEqual(skill.Skill_Desc, updated_desc)

    def test_delete_skill(self):
        # Test data
        skill_data = {
            'Skill_Name': 'Python',
            'Skill_Desc': 'A high-level programming language.'
        }
        skill = Skill(skill_name=skill_data['Skill_Name'], skill_desc=skill_data['Skill_Desc'])

        # Simulate deleting the skill
        self.db_session.delete(skill)
        self.db_session.commit()

        # Test that delete and commit were called
        self.db_session.delete.assert_called_with(skill)
        self.db_session.commit.assert_called_once()

    def tearDown(self):
        self.db_session.reset_mock()

if __name__ == '__main__':
    unittest.main()