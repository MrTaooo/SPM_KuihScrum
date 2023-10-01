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
    ('Software Developer', 'Web development'),
    ('Software Developer', 'API integration'),
    ('Software Developer', 'Debugging'),
    ('Data Analyst', 'Data analysis'),
    ('Data Analyst', 'SQL'),
    ('Data Analyst', 'Data mining'),
    ('Marketing Specialist', 'Content marketing'),
    ('Marketing Specialist', 'Branding'),
    ('Marketing Specialist', 'Public relations'),
    ('Sales Representative', 'Relationship building'),
    ('Sales Representative', 'Product knowledge'),
    ('Sales Representative', 'Communication skills');

-- Insert data into Role_Skill table 
INSERT INTO Accessrights (Access_ID, Access_type)
VALUES
    ('0', 'Staff'),
    ('1', 'HR');

    -- Insert data into Staff table 
INSERT INTO Staff (Staff_ID, Staff_FName, Staff_LName, Dept, Country, Email, Access_Rights)
VALUES
    ('01385970', 'Lin', 'Tao', 'Engineering', 'United States', 'lintao@gmail.com', '1'),
    ('01387909', 'Chery', 'Lim', 'Business', 'Korea', 'limcheryl@gmail.com', '1'),
    ('01439201', 'John', 'Lee', 'Accounting', 'Malaysia', 'johnlee99@gmail.com', '1'),
    ('01523071', 'Ignatious', 'Goh', 'IT Support', 'China', 'ignatiousgoh@gmail.com', '1');

-- Insert data into Staff_Skill table 
INSERT INTO Staff_Skill (Staff_ID, Skill_Name)
VALUES
    ('01385970', 'Data mining'),
    ('01385970', 'API integration'),
    ('01385970', 'Debugging'),
    ('01387909', 'Data analysis'),
    ('01387909', 'Product knowledge'),
    ('01387909', 'Data mining'),
    ('01439201', 'Content marketing'),
    ('01439201', 'Branding'),
    ('01439201', 'API integration'),
    ('01523071', 'Relationship building'),
    ('01523071', 'SQL'),
    ('01523071', 'Communication skills');
