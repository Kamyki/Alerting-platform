#!/usr/bin/env python3

from dkron import Dkron

hosts = ['http://localhost:8080']
api = Dkron(hosts)
print(dir(api))
# exit(1)
print(api.get_jobs()) # ('my-dkron-job')['error_count'])
api.run_job('date')
