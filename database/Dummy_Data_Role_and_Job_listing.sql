USE SPM_KUIH;

-- Insert data into the Role table
INSERT INTO Role (Role_Name, role_desc)
VALUES
    ('Software Developer', 'Responsible for developing software applications and systems.'),
    ('Data Analyst', 'Analyzes data to provide insights and support decision-making.'),
    ('Marketing Specialist', 'Plans and executes marketing campaigns and strategies.'),
    ('Sales Representative', 'Sells products or services to customers and clients.');

-- Insert data into the Job_Listing table
INSERT INTO Job_Listing (Role_Name, publish_Date, Closing_date)
VALUES
    ('Software Developer', '2023-09-01', '2023-09-15'),
    ('Data Analyst', '2023-09-02', '2023-09-16'),
    ('Marketing Specialist', '2023-09-03', '2023-09-17'),
    ('Sales Representative', '2023-09-04', '2023-09-18'),
    ('Software Developer', '2023-09-05', '2023-09-19');

-- Insert data into Role_Skill table 
INSERT INTO Role_Skill (Role_Name, Skill_Name)
VALUES
    ('Software Developer', 'Web development, API integration, Debugging'),
    ('Data Analyst', 'Data analysis, SQL, Data mining'),
    ('Marketing Specialist', 'Content marketing, Branding, Public relations'),
    ('Sales Representative', 'Relationship building, Communication skills, Product knowledge');
