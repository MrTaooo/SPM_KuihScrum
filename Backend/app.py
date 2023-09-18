from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

# -------------- Import for Notification Service (START) --------------
import amqp_setup
import pika
import json
# --------------- Import for Notification Service (End) ---------------

# -------------- Import for Job Listing /createlisting (START) --------------
from datetime import datetime
# -------------- Import for Job Listing /createlisting (END) --------------
app = Flask(__name__)


# Process job listing creation 
@app.route('/createlisting', methods=['POST'])
def process_data():
    data = request.get_json()
    roletitle = data["roletitle"] 
    closingdate = data["closingdate"]
    date = datetime.now()
    if (closingdate < date): 
        return "Error, closing date cannot be the day before "
    # elif (roletitle in (db) and closing date in (db)): 
    #     return "Error, cannot have duplicate listings"
 
    # Return a response, for example, a confirmation message
    else: 
        return jsonify({"message": "Data received and processed successfully"})


if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000, debug=True)
