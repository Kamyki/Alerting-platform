from dkron import Dkron
from mongo import get_services

def ERROR(x):
    print("==== " + str(x))
    exit(1)


def read_yaml(filename):
    import yaml
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            ERROR(exc)


if __name__ == "__main__":
    hosts = ['http://localhost:8080']
    api = Dkron(hosts)

    services = get_services()
    #print(list(services))
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
