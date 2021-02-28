# Alerting-platform
IRIO 2020, alerting platform for monitoring urls availability.

Based on [dkron](https://dkron.io/) (distributed job scheduler, node fault-tolerant, easily scalable) and [MongoDB Atlas database](https://www.mongodb.com/cloud/atlas), also easily scalable and fault-tolerant. Both solutions are based on **Kubernetes** and are easily deployable on *Google Cloud Platform*.


Brief descriptions of sources:

* `admin_api/admin_cancel_incident.py` - as params it take URL and unique token that is being generated during incident detection, admin runs it to send request for MongoDB database to cancel incident.
* `admin_api/admin_incident_endpoints.py` - source code of server that receives requests sent nby `admin_cancel_incident.py` and requests database.
* `admin_api/db_tests.py` - unit tests of database and simple use cases; incident reporting, incident cancelling by admin etc.
* `kubernetes/*` - deployment files for k8s
* `primer/*` - boot process of whole architecture, running first jobs on `dkron` based on database services list.
* `worker/worker.py` - script run each `frequency` seconds for each service; it checks URL availability, if it sees that it doesn't work longer than `alerting window` it sends email to first admin and schedules `reporter.py`, that will check whether time for response for admin1 exceeded
* `worker/reporter.py` - scheduled by `worker.py`, it checks whether `admin1` cancelled incident; if he didn't and `allowed_response_time` exceeded, it reports `admin2`
