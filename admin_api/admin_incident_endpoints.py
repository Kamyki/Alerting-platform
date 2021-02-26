#!/usr/bin/env python3

from flask import request, Flask
app = Flask(__name__)

@app.route('/cancel', methods=["POST"])
def hello_world():
    # following subscription with return HTTP400 in case of params not passed
    token = request.form['token']
    url = request.form['url']

    admin_deactivate_alert(url)
    return f"OK"


@app.route('/health', methods=["GET"])
def health():
    return f"OK"


if __name__ == '__main__':
    app.run()
