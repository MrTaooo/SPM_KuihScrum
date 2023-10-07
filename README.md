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

**templates:** Stores the HTML files. 

**tests:** Stores the Selenium test scripts. 

## Files Explaination

**sqlalchemy_define:** This python file is used to create a Flask web application and configures it to connect to a MySQL database using SQLAlchemy. 

## Installation

Use the package manager [pip] to install the required dependencies required to run the project listed in the requirements.txt file. Please install Python before installing the dependencies. 

```bash
pip install -r requirements.txt
```

## Usage

**Step 1:** Run WAMP

**Step 2:** Open MySQL workbench and run the SQL scripts. Alternatively, go to myphp Admin and create the database there. The SQL scripts are provided in the project under the database folder. 

**Step 3:** Run app.py

**Step 4:** Run index.html in the templates folder. 