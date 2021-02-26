#!/usr/bin/env python3

import multiprocessing
import time
import requests
import argparse
from requests.exceptions import MissingSchema, InvalidSchema
from mongo import *

PING_FREQ_SEC = 1

parser = argparse.ArgumentParser(description="I'm worker script")
# 'frequency' param is not needed inside that script, because it's already scheduled in cyclic way.
parser.add_argument('--url', help='URL to check', required=True)

args = parser.parse_args()

URL = args.url

# === enable debug mode
DEBUG = True

LOG = lambda x : print(f"=== {x}") if DEBUG else True

def ERROR(x):
    print(f"ERROR!: {x}")
    exit(1)

def MAIN_FUNC(url, timeout):
    while True:
        try:
            requests.get(url, timeout=1)
            # ok, request completed, finish healt check
            LOG(f"Service {url} healthy!")
            break
        except (MissingSchema, InvalidSchema):
            ERROR("Malformed URL! Please add 'http(s)://' prefix to passed --url!")
        except:
            # TODO type of exception (timeout or wrong domain)
            LOG(f"Service {url} unavailable, checking until --alerting-window={timeout} seconds passes..")
            time.sleep(PING_FREQ_SEC)

def schedule_reporter_job(url):
    LOG("dummy Reporter Job scheduling..")
    pass


def report_incident(url):
    LOG("incident reporting..")
    put_incident(url)
    # after putting persistent entry let's schedule dkron job
    schedule_reporter_job(url)


if __name__ == '__main__':

    service = get_service(URL)
    if service is None:
        ERROR(f"Unknown service! {URL} service not found in database")
    WINDOW_SEC = service['alerting_window']

    p = multiprocessing.Process(target=MAIN_FUNC, args=(URL, WINDOW_SEC))
    p.start()

    # After `alerting_window` seconds check whether process finished successfully
    p.join(WINDOW_SEC)

    if p.is_alive():
        p.terminate()

    if p.exitcode is None:
        LOG(f'Oops, {URL} timeouts! Incident will be reported.')
        # ====================== TODO
        # schedule job of reporting to admin
        report_incident(URL)
        exit(1)
    elif p.exitcode != 0:
        exit(p.exitcode) # TODO (maybe wrong) assumption: wrong arguments (i.a. malformed URL), incident will not be reported in that case
    else:
        LOG(f"OK, {p} finished successfully!")
        exit(0)
