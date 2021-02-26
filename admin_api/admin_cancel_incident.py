#!/usr/bin/env python3


import requests
import multiprocessing
import time
import argparse
from requests.exceptions import MissingSchema, InvalidSchema

PING_FREQ_SEC = 1

parser = argparse.ArgumentParser(description="Incident cancellation script. Sends POST request for given url with given token.")
parser.add_argument('--reported_url', help='URL of dead reported service.', required=True)
parser.add_argument('--token', help='Auth token to cancel incident', required=True)
parser.add_argument('--endpoint', help='Cancellation endpoint (http://ADDR:PORT)', required=True)

args = parser.parse_args()

URL = args.reported_url
TOKEN = args.token
ENDPOINT = args.endpoint

# === enable debug mode
DEBUG = True

LOG = lambda x : print(f"=== {x}") if DEBUG else True

def ERROR(x):
    print(f"ERROR!: {x}")
    exit(1)

response = requests.post(ENDPOINT, data={'url': URL, 'token': TOKEN})

# True if no error, False otherwise
def handle_response(response):
    return response.ok

if handle_response(response):
    print("OK, incident cancelled successfully!")
else:
    print(f"The error occured while incident cancelling. Status code: {response.status_code}. Try once again!")