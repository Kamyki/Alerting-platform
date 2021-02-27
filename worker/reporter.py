#!/usr/bin/env python3

import multiprocessing
import time
import requests
import argparse
from requests.exceptions import MissingSchema, InvalidSchema
from datetime import datetime

# local imports 
from utils import *
from mongo import *

parser = argparse.ArgumentParser(description="I'm reporter script")
parser.add_argument('--url', help='URL whose check failed.', required=True)

args = parser.parse_args()

FAIL_URL = args.url


if __name__ == "__main__":
    # ok, so im generic process called after first admin was reported by `worker.py`.

    service = get_service(FAIL_URL)
    first_admin_email = get_first_admin_email(service)
    second_admin_email = get_second_admin_email(service)
    token = get_incident_token_second_admin(FAIL_URL)

    report = should_report_second_admin(FAIL_URL)
    LOG(f"reporter.py: should_report_second_admin({FAIL_URL}) == {report}")
    if report:
        db[INCIDENTS_COLLECTION_NAME].update_one({"url": FAIL_URL, "active": True}, {"$set": {"reported_second_admin": True}})
        send_email(first_admin_email, token, FAIL_URL)
