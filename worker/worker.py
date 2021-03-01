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

def check_alerting_window_exceeded(service):
    last_ok = service['last_ok_visited_timestamp']
    alerting_window = service['alerting_window']
    now = datetime.datetime.now()

    if last_ok is None:
        LOG(f"First check? Start counting from now!")

        db[SERVICES_COLLECTION_NAME].update_one({"url": URL}, {"$set": {"last_ok_visited_timestamp": now}})
    else:
        if datetime.timedelta(seconds=alerting_window) <= (now - last_ok):
            report_incident(service)
        else:
            LOG(f"Seems fine: alerting window: {alerting_window}, now - last_ok: {now - last_ok}")



def main_func(service):
    success = False
    try:
        requests.get(URL, timeout=1)
        # ok, request completed, finish healt check
        success = True
        LOG(f"Service {URL} healthy!")
    except (MissingSchema, InvalidSchema):
        success = True
        ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
    except Exception:
        success = False
        LOG(f"Service {URL} unavailable! Checking if 'alerting_window' exceed...")

    if not success:
        check_alerting_window_exceeded(service)


def schedule_reporter_job(service):
    LOG("dummy Reporter Job scheduling..")
    api = Dkron([DKRON_ADDRESS])
    alerting_window = service['alerting_window']
    api.apply_job({
        "schedule": f'@at {datetime.datetime.now() + datetime.timedelta(seconds=10)}',
        "name": str(service['_id']),

        "timezone": "Europe/Warsaw",
        "owner": "Alerting Platform",
        "executor": "shell",
        "executor_config": {
          "command": f'python3 /app/reporter.py --url {service["url"]}'
        },
       "processors": {
         "log": {
           "forward": "true"
         }
       },
       "tags": {
          "worker": "crawler:1"
       }
    })
    pass


def report_incident(service):
    if get_incident(URL) is None:
        LOG("incident reporting: True (first time)")
        put_incident(URL)
        first_admin_email = get_first_admin_email(service)
        token = get_incident_token_first_admin(URL)
        send_email(first_admin_email, token, URL)

        # schedule dkron job
        schedule_reporter_job(URL)
    else:
        LOG("incident reporting: False (already reported)")



if __name__ == '__main__':
    LOG(f"worker.py: checking service {URL}...")
    service = get_service(URL)
    if service is None:
        ERROR(f"Unknown service! {URL} service not found in database")

    main_func(service)
