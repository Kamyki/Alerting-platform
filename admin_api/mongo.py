#!/usr/bin/python3

import pymongo
from pprint import pprint

pt = lambda x: print(type(x))
pd = lambda x: pprint(dir(x))
pdoc = lambda x: pprint(x.__doc__)
p = lambda x: pprint(x)

def ERROR(x):
    print(x)
    exit(1)

DEBUG = True

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

client = pymongo.MongoClient(MONGO_CONNECTION_KEY)
db = client[DB_NAME]
# collection = db[COLLECTION_NAME]

SERVICES_YAML_PATH="services.yaml"


def populate_services(
        entries_list,
        db=db, 
        services_collection_name=SERVICES_COLLECTION_NAME):
    LOG(entries_list)
    db.drop_collection(services_collection_name)
    collection = db[services_collection_name]
    collection.insert_one(entries_list)

def get_services(
        db=db,
        services_collection_name=SERVICES_COLLECTION_NAME):
    collection = db[services_collection_name]
    services = collection.find_one({})['services']
    LOG(services)
    return services


populate_services(read_yaml(SERVICES_YAML_PATH))
get_services()

