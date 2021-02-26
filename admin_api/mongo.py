#!/usr/bin/python3

import pymongo
from pprint import pprint
import datetime

pt = lambda x: print(type(x))
pd = lambda x: pprint(dir(x))
pdoc = lambda x: pprint(x.__doc__)
p = lambda x: pprint(x)

def ERROR(x):
    print("==== " + str(x))
    exit(1)

DEBUG = True

if DEBUG:
    print("=== DEBUG variable set, output will be verbose...\n")


LOG = lambda x : print("==== " + str(x)) if DEBUG else True

def read_yaml(filename):
    import yaml
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            ERROR(exc)

db_creds = read_yaml("secret.yaml")
DB_USER = db_creds["db_user"]
DB_PSWD = db_creds["db_password"]
del db_creds

MONGO_CONNECTION_KEY=client = f"mongodb+srv://{DB_USER}:{DB_PSWD}@klaster.jbd28.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

DB_NAME = "irio"
SERVICES_COLLECTION_NAME = "services"
ADMINS_COLLECTION_NAME = "admins"
INCIDENTS_COLLECTION_NAME = "incidents"

client = pymongo.MongoClient(MONGO_CONNECTION_KEY)
db = client[DB_NAME]
# collection = db[COLLECTION_NAME]

SERVICES_YAML_PATH="services.yaml"
ADMINS_YAML_PATH="admins.yaml"
INCIDENTS_YAML_PATH="incidents.yaml"

# =========================== GENERIC

def populate_collection(
        single_entry,
        collection,):
    LOG("populating " + str(single_entry))
    collection.drop()
    collection.insert_many(single_entry)


# =========================== SERVICES

def populate_services(
        services,
        db=db, 
        services_collection_name=SERVICES_COLLECTION_NAME):
    populate_collection(services, db[services_collection_name])

def get_services(
        db=db,
        services_collection_name=SERVICES_COLLECTION_NAME):
    collection = db[services_collection_name]
    services = collection.find({})
    LOG(services)
    return services


# =========================== ADMINS
def populate_admins(
        admins,
        db=db, 
        admins_collection_name=ADMINS_COLLECTION_NAME):
    populate_collection(admins, db[admins_collection_name])

def get_admins(
        db=db,
        admins_collection_name=ADMINS_COLLECTION_NAME):
    collection = db[admins_collection_name]
    admins = collection.find({})
    LOG(admins)
    return admins

def __get_admin_email(
        first,
        service,
        db,
        admins_collection_name,
        services_collection_name):
    collection = db[admins_collection_name] # ['admins']
    admin_id = service['first_admin'] if first else service['second_admin']
    # res = collection.find_one({'admins.name': admin_id}, {"admins.$"}) # second param is projection
    res = collection.find_one({'name': admin_id})
    if res is None:
        ERROR(f"Database inconsistency! Couldn't find matching administrator with name '{admin_id}' in '{admins_collection_name}' collection!")
    res = res['email'] # cursed
    return res
    
def get_first_admin_email(
        service,
        db=db, 
        admins_collection_name=ADMINS_COLLECTION_NAME,
        services_collection_name=SERVICES_COLLECTION_NAME):
    return __get_admin_email(True, service, db, admins_collection_name, services_collection_name)

def get_second_admin_email(
        service,
        db=db, 
        admins_collection_name=ADMINS_COLLECTION_NAME,
        services_collection_name=SERVICES_COLLECTION_NAME):
    return __get_admin_email(False, service, db, admins_collection_name, services_collection_name)


# =========================== INCIDENTS

def populate_incidents(
        incidents,
        db=db, 
        incidents_collection_name=INCIDENTS_COLLECTION_NAME):
    populate_collection(incidents, db[incidents_collection_name])

def get_incidents(
        db=db,
        incidents_collection_name=INCIDENTS_COLLECTION_NAME):
    collection = db[incidents_collection_name]
    incidents = list(collection.find({})) # ['incidents']
    LOG(incidents)
    return incidents

# we cannot use pure 'read_yaml' for incidents, need to set 'datetime' field.
def read_yaml_incidents(path=INCIDENTS_YAML_PATH):
    lst = read_yaml(path)
    for el in lst:
        el['datetime'] = datetime.datetime.now()
    return lst

# returns active incident for given URL if any, otherwise None.
def get_incident(
        url,
        db=db,
        incidents_collection_name=INCIDENTS_COLLECTION_NAME):
    collection = db[incidents_collection_name]
    incident = collection.find_one({"url": url, "active": True})
    if incident is None:
        return None
    LOG(incident)
    return incident


# call in case of service unreachable detected.
# TODO should use replace_one for atomicity
def put_incident(
        url,
        db=db,
        incidents_collection_name=INCIDENTS_COLLECTION_NAME,
        services_collection_name=SERVICES_COLLECTION_NAME):
    service = db[services_collection_name].find_one({"url": url})
    if service is None:
        ERROR(f"Database inconsistency detected! No service {url} present!")
    collection = db[incidents_collection_name]
    assert get_incident(url, db, incidents_collection_name) is None # that's a bit crappy check..
    entry = {
        'active': True,
        'datetime': datetime.datetime.now(),
        'url': url,
        'reported_second_admin': False,
    }

    insert_res = collection.replace_one({"url": url}, entry)
    p(insert_res)
    
    LOG(f"DB populated with new incident: {entry}")


# idempotent, may be called several times
def admin_deactivate_alert(
        url,
        db=db,
        incidents_collection_name=INCIDENTS_COLLECTION_NAME):
    collection = db[incidents_collection_name]
    collection.update_one({"url": url}, {"$set": {"active": False}})
    LOG(f"Alert for {url} deactivated!")


# returns True if event active, admin1 already reported and timeouted (>= allowed_response_time)
def should_report_second_admin(
        url,
        db=db,
        incidents_collection_name=INCIDENTS_COLLECTION_NAME,
        services_collection_name=SERVICES_COLLECTION_NAME,
        ):
    service = db[services_collection_name].find_one({"url": url})
    if service is None:
        ERROR(f"Database inconsistency detected! No service {url} present!")
    incident = get_incident(url, db, incidents_collection_name)
    if incident is None:
        return False
    allowed_response_time = datetime.timedelta(seconds=service['allowed_response_time'])
    import time
    return not incident['reported_second_admin'] and datetime.datetime.now() - incident['datetime'] >= allowed_response_time
        
