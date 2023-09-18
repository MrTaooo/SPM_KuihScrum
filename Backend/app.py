from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

# -------------- Import for Notification Service (START) --------------
import amqp_setup
import pika
import json
# --------------- Import for Notification Service (End) ---------------