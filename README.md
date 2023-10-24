# Skill-Based Role Portal

A self-help portal for staff to apply for jobs, and HR to create job listings and view applicants for each job. 

## Version 
As this is currently version 2.1, it has yet to be deployed onto a remote server to be run online. 

## Language Used
Frontend
- HTML, CSS, JavaScript

Backend
- Python 

## Database
Uses MySQL, a Relational Database Management System (RDMS).

## Frameworks Used
Frontend
- Vue.js using CDN 
- Bootstrap Version 5.3.1 using CDN

Backend
- Python Flask

## Library Used
- Date range picker library 
- Popper library for dropdown menu
- Axios library to make HTTP requests

## Folders Explanation
**database:** Stores the SQL scripts to create the database and tables. Dummy data are also provided. 

**models:** SQLAlchemy model classes for working with databases created in MySQL. 1 file is for 1 model class. 

**routes:** Stores function files that are imported by app.py to tie the function to an API endpoint. 1 file is for 1 function. 

**static:** Stores the main CSS file for the application. Also stores the JavaScripts which creates the Vue application instance. 

**templates:** 
Stores:
- HTML files
- Javascript files
- CSS files

**tests:** Stores the Selenium test scripts. 

## Files Explaination

**sqlalchemy_define:** This python file is used to create a Flask web application and configures it to connect to a MySQL database using SQLAlchemy. 

## Installation

Use the package manager [pip] to install the required dependencies required to run the project listed in the requirements.txt file. Please install Python before installing the dependencies. 

```bash
pip install -r requirements.txt
```

## IDE Extensions
- Install the LiveServer extension (extension ID in VS Code: ritwickdey.LiveServer) 

## Usage
**Step 1:** Run WAMP/MAMP

**Step 2:** Open MySQL workbench and run the SQL scripts. Alternatively, go to myphp Admin and create the database there. The SQL scripts are provided in the project under the database folder. 

**Step 3:** Run app.py

**Step 4:** Run live server extension

**Step 4:** Enter this url to run the website: http://127.0.0.1:5500/templates/index.html. Note that the port number should match the port number given after running the live server extension. 

## Coding Notes:
- The index.js and manage.js are module types, to run the files successfully, do declare the variables before using them. (E.g. var foo = "Foo")

## Running of Selenium Test Scripts


### Running Locally
**Step 1:**: Uncomment this code (line 19 in test_script.py) in the tests/end_to_end folder. --> driver.get("http://127.0.0.1:5500/templates/index.html")

**Step 2:**: Comment this code (line 20 in test_script.py) in the same folder. --> driver.get("https://spm-kuih-scrum.vercel.app/")

**Step 3:** Uncomment all the function calls at the end of test_script.py

**Step 4:** Run test_data.sql in the database folder in MySql (this acts as a setup for the testing process)

**Step 4:** Run the python script in terminal

### Running on GitHub Actions
**Step 1:**: Comment this code (line 19 in test_script.py) in the tests/end_to_end folder. --> driver.get("http://127.0.0.1:5500/templates/index.html")

**Step 2:**: Uncomment this code (line 20 in test_script.py) in the same folder. --> driver.get("https://spm-kuih-scrum.vercel.app/")

**Step 3:** Comment all the function calls at the end of test_script.py

**Step 4:** Push local repository to GitHub repository