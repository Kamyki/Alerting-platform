#!/usr/bin/env python3

import multiprocessing
import time
import requests
import argparse
from requests.exceptions import MissingSchema, InvalidSchema
from mongo import *
import datetime
from utils import *

PING_FREQ_SEC = 1

parser = argparse.ArgumentParser(description="I'm worker script")
# 'frequency' param is not needed inside that script, because it's already scheduled in cyclic way.
parser.add_argument('--url', help='URL to check', required=True)

args = parser.parse_args()

URL = args.url

def check_alerting_window_exceeded(url):
    service = get_service(url)
    last_ok = service['last_ok_visited_timestamp']
    now = datetime.datetime.now()
    if last_ok is None:
        db[SERVICES_COLLECTION_NAME].update_one({"url": url}, {"last_ok_visited_timestamp": now})
    else:
        if datetime.timedelta(seconds=WINDOW_SEC) >= (last_ok - now):
            report_incident(url)


def main_func(url, timeout=1):
    try:
        requests.get(url, timeout=timeout)
        # ok, request completed, finish healt check
        LOG(f"Service {url} healthy!")
    except (MissingSchema, InvalidSchema):
        ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
    except:
        LOG(f"Service {url} unavailable! Checking if 'alerting_window' exceed...")
        check_alerting_window_exceeded(url)


def schedule_reporter_job(url):
    LOG("dummy Reporter Job scheduling..")
    pass


def report_incident(url):
    LOG("incident reporting..")
    put_incident(url)
    first_admin_email = get_first_admin_email(service)
    token = get_incident_token_first_admin(URL)
    send_email(first_admin_email, token, URL)
    
    # schedule dkron job
    schedule_reporter_job(url)


if __name__ == '__main__':
    service = get_service(URL)
    if service is None:
        ERROR(f"Unknown service! {URL} service not found in database")
    WINDOW_SEC = service['alerting_window']

    main_func(URL, WINDOW_SEC)