#!/usr/bin/env python3

import multiprocessing
import time
import requests
import argparse
from requests.exceptions import MissingSchema, InvalidSchema

PING_FREQ_SEC = 1

parser = argparse.ArgumentParser(description="I'm worker script")
# 'frequency' param is not needed inside that script, because it's already scheduled in cyclic way.
parser.add_argument('--url', help='URL to check', required=True)
parser.add_argument('--alerting-window', help='Time of helath checking; When service does not respond longer than alerting-window seconds, then schedule reporting task.', required=True)

args = parser.parse_args()

URL = args.url
WINDOW_SEC = int(args.alerting_window)

# === enable debug mode
DEBUG = True

LOG = lambda x : print(f"=== {x}") if DEBUG else True

def ERROR(x):
    print(f"ERROR!: {x}")
    exit(1)

def MAIN_FUNC(url=URL, timeout=WINDOW_SEC):
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

    

def report_incident(url):
    LOG("dummy incident reporting..")


if __name__ == '__main__':
    p = multiprocessing.Process(target=MAIN_FUNC)
    p.start()

    # Wait for 2 seconds or until process finishes
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

