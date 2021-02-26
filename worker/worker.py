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
    alerting_window = service['alerting_window']
    now = datetime.datetime.now()

    if last_ok is None:
        LOG(f"First check? Start counting from now!")

        db[SERVICES_COLLECTION_NAME].update_one({"url": url}, {"$set": {"last_ok_visited_timestamp": now}})
    else:
        if datetime.timedelta(seconds=alerting_window) <= (now - last_ok):
            LOG(f"Report incident!")
            report_incident(url)
        else:
            LOG(f"Seems fine: alerting window: {alerting_window}, now - last_ok: {now - last_ok}")



def main_func(url):
    success = False
    try:
        requests.get(url, timeout=1)
        # ok, request completed, finish healt check
        success = True
        LOG(f"Service {url} healthy!")
    except (MissingSchema, InvalidSchema):
        success = True
        ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
    except Exception:
        success = False
        LOG(f"Service {url} unavailable! Checking if 'alerting_window' exceed...")

    if not success:
        check_alerting_window_exceeded(url)


def schedule_reporter_job(url):
    LOG("dummy Reporter Job scheduling..")
    api = Dkron([DKRON_ADDRESS])

    # api.apply_job({
    #     "schedule": f'@once',
    #     "name": str(service['_id']),
    #
    #     "timezone": "Europe/Warsaw",
    #     "owner": "Alerting Platform",
    #     "executor": "shell",
    #     "executor_config": {
    #       "command": f'python3 /app/worker.py --url {service["url"]}'
    #     },
    #    "processors": {
    #      "log": {
    #        "forward": "true"
    #      }
    #    }
    # })
    pass


def report_incident(url):
    LOG("incident reporting..")
    if get_incident(url) is None:
        put_incident(url)
        first_admin_email = get_first_admin_email(service)
        token = get_incident_token_first_admin(URL)
        send_email(first_admin_email, token, URL)

        # schedule dkron job
        schedule_reporter_job(url)


if __name__ == '__main__':
    DEBUG = True
    service = get_service(URL)
    LOG(f"worker.py: checking service {URL}...")
    if service is None:
        ERROR(f"Unknown service! {URL} service not found in database")

    main_func(URL)
