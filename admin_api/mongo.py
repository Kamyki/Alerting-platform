#!/usr/bin/python3

import pymongo
from pprint import pprint

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


LOG = lambda x : pprint(x) if DEBUG else True

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

client = pymongo.MongoClient(MONGO_CONNECTION_KEY)
db = client[DB_NAME]
# collection = db[COLLECTION_NAME]

SERVICES_YAML_PATH="services.yaml"
ADMINS_YAML_PATH="admins.yaml"


def populate_collection(
        single_entry,
        collection,):
    LOG("populating " + str(single_entry))
    collection.drop()
    collection.insert_one(single_entry)


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
    services = collection.find_one({})['services']
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
    admins = collection.find_one({})['admins']
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
    res = collection.find_one({'admins.name': admin_id}, {"admins.$"}) # second param is projection
    if res is None:
        ERROR(f"Database inconsistency! Couldn't find matching administrator with name '{admin_id}' in '{admins_collection_name}' collection!")
    res = res['admins'][0]['email'] # cursed
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

