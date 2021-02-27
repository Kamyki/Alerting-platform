#!/usr/bin/env python3

from flask import request, Flask
app = Flask(__name__)


from mongo import *

@app.route('/cancel', methods=["POST"])
def hello_world():
    # following subscription with return HTTP400 in case of params not passed
    token = request.form['token']
    url = request.form['url']

    res = admin_deactivate_alert(url, token)
    if (res):
        msg = "OK, incident resolved successfully!"
        return msg, 200
    else:
        msg = "Error during incident resolving occured! Exiting.."
        LOG(msg)
        return (msg, 400)


@app.route('/health', methods=["GET"])
def health():
    return f"OK"


if __name__ == '__main__':
    app.run()
