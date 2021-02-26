#!/usr/bin/env python3

import multiprocessing
import time
import requests
import argparse
from requests.exceptions import MissingSchema, InvalidSchema
from datetime import datetime

# That script is generic - may be used by both first and second admin notification job
# It performs following steps:
# * checks in DB whteher there exists incident entry.
# * if exists, checks it's timestamp. If it's low enough, emails second admin.
# * if doesn't exist, it means that it is first try. Puts entry in DB and email first admin.

parser = argparse.ArgumentParser(description="I'm reporter script")
parser.add_argument('--url', help='URL whose check failed.', required=True)
parser.add_argument('--first_admin_email', help='Email addr of admin1.', required=True)
parser.add_argument('--second_admin_email', help='Email addr of admin2.', required=True)
parser.add_argument('--get_entry_endpoint', help='Endpoint of GET incident entry.', required=True)
parser.add_argument('--put_entry_endpoint', help='Endpoint of GET incident entry.', required=True)
parser.add_argument('--allowed_response_time_endpoint', help='Endpoint of Allowed Response Time for first admin', required=True)

args = parser.parse_args()

FAIL_URL = args.url,
FIRST_ADMIN_EMAIL = args.second_admin_email,
SECOND_ADMIN_EMAIL = args.second_admin_email,
GET_ENTRY_ENDPOINT = args.get_entry_endpoint
PUT_ENTRY_ENDPOINT = args.put_entry_endpoint
ALLOWED_RESPONSE_TIME = args.allowed_response_time_endpoint

# === enable debug mode
DEBUG = True

LOG = lambda x : print(f"=== {x}") if DEBUG else True

def ERROR(x):
    print(f"ERROR!: {x}")
    exit(1)


class Entry:
    timestamp = datetime.now()

# returns Entry if entry exist, None otherwise.
# raises error if DB unavailable.
def db_check_incident_entry(
    get_entry_endpoint=GET_ENTRY_ENDPOINT,
    ):
    try:
        response = requests.get(get_entry_endpoint, timeout=1).json()
    except (MissingSchema, InvalidSchema):
        ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
    except:
        # TODO type of exception (timeout or wrong domain)
        ERROR(f"Database Service GET endpoint '{get_entry_endpoint}' unavailable!")

    LOG("dummy checking whether db response contains entry...")
    
    # TODO === parse response and return True or False
    LOG("assume it contains entry, return True")
    return Entry

# TODO params
def db_put_incident_entry(
    put_entry_endpoint=PUT_ENTRY_ENDPOINT,
    ):
    try:
        response = requests.get(put_entry_endpoint, timeout=1).json()
    except (MissingSchema, InvalidSchema):
        ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
    except:
        # TODO type of exception (timeout or wrong domain)
        ERROR(f"Database Service GET endpoint '{put_entry_endpoint}' unavailable!")


FROM = "matinekbot@gmail.com"
FROM_PW = "IRIO2021"

def send_email(addr, dead_url):
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, FROM_PW)

    msg = f"Hey, admin! Your service {dead_url} is dead! Please fix it and confirm you saw this message!"
    server.sendmail("HEALTH WIZARD", addr, msg)
    
    LOG(f"INFO: Email to '{addr}' sent successfully!")


# returns True if we should inform admin2, False otherwise
def admin1_timeout(entry_timestamp, allowed_response_time=ALLOWED_RESPONSE_TIME):
    LOG("dummy admin1_timeout: return True (yes, inform admin2)")
    return True

if __name__ == "__main__":
    entry = db_check_incident_entry()

    if not entry is None:
        timestamp = entry.timestamp
        # ... check, whether ALLOWED_RESPONSE_TIME fits
        report_admin2 = admin1_timeout(timestamp)
        if report_admin2:
            send_email(SECOND_ADMIN_EMAIL, FAIL_URL)
    else:
        # none entry
        db_put_incident_entry()
        send_email(FIRST_ADMIN_EMAIL, FAIL_URL)

