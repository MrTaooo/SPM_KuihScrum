from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_cors import CORS
import platform
    
db = SQLAlchemy()
DB_NAME = "database.db"
    
    
def create_app():
    app = Flask(__name__)
    CORS(app)

    # -------------- Connection to mySQL DB --------------
    def check_os():
        system = platform.system()  # Get the name of the operating system
        if system == 'Windows':
            return 'mysql+mysqlconnector://root@localhost:3306/SPM_KUIH'  # For Windows
        elif system == 'Darwin':
            return 'mysql+mysqlconnector://root:root@localhost:3306/SPM_KUIH'  # For macOS
        else:
            # to run in GitHub actions after creating the db in GitHub actions 
            return 'mysql+mysqlconnector://root:root@localhost:3306/SPM_KUIH'
        
    # Set the URI based on the OS
    app.config['SQLALCHEMY_DATABASE_URI'] = check_os()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    # Initialize the SQLAlchemy database with the Flask app
    db.init_app(app)
    
    # Import and register your routes and blueprints here if needed
    
    return app