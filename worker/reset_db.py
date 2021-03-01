from dkron import Dkron
from mongo import *
from utils import read_yaml, LOG, DKRON_ADDRESS, SERVICES_YAML_PATH, ADMINS_YAML_PATH
from time import sleep

def reset_db():

    db[INCIDENTS_COLLECTION_NAME].drop()
    db[ADMINS_REACTION_COLLECTION_NAME].drop()
    db[SERVICES_COLLECTION_NAME].drop()
    db[ADMINS_COLLECTION_NAME].drop()
    populate_services(read_yaml(SERVICES_YAML_PATH))
    populate_admins(read_yaml(ADMINS_YAML_PATH))


reset_db()
