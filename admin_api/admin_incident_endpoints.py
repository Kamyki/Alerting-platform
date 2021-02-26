#!/usr/bin/env python3

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/cancel', methods=["POST"])
def hello_world():
    # following subscription with return HTTP400 in case of params not passed
    token = request.form['token']
    url = request.form['url']
    
    admin_deactivate_alert(url
    return f"OK"
