from dkron import Dkron
from mongo import *
from utils import read_yaml, LOG, DKRON_ADDRESS


if __name__ == "__main__":
    db[INCIDENTS_COLLECTION_NAME].drop()
    db[ADMINS_REACTION_COLLECTION_NAME].drop()
    db[SERVICES_COLLECTION_NAME].drop()
    db[ADMINS_COLLECTION_NAME].drop()
    populate_services(read_yaml(SERVICES_YAML_PATH))
    populate_admins(read_yaml(ADMINS_YAML_PATH))

    #TODO stop previous jobs
    hosts = [DKRON_ADDRESS]
    api = Dkron(hosts)

    jobs = [x['id'] for x in api.get_jobs()]
    LOG("Delete jobs")
    for job in jobs:
        api.delete_job(job)
        LOG(f'Deleted {job}')

    services = get_services()
    LOG("Start scheduling jobs")
    for service in services:
        api.apply_job({
            "schedule": f'@every { service["frequency"] }s',
            "name": str(service['_id']),

            "timezone": "Europe/Warsaw",
            "owner": "Alerting Platform",
            "executor": "shell",
            "executor_config": {
              "command": f'python3 /app/worker.py --url {service["url"]}'
            },
           "processors": {
             "log": {
               "forward": "true"
             }
           }
        })
        LOG(f'Scheduled {service["url"]}')
