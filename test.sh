docker build -t alerting-platform/test -f admin-api/Dockerfile ./admin-api
docker build -t alerting-platform/worker -f worker/Dockerfile ./worker


docker run -p 8080:8080 --name dkron --rm -d alerting-platform/worker \
 dkron agent --server --bootstrap-expect=1 --retry-join "provider=k8s label_selector=\"app=dkron,component=server\""

sleep 10

curl localhost:8080/v1/jobs -XPOST -d '{
   "name": "job2",
   "schedule": "@every 10s",
   "timezone": "Europe/Berlin",
   "owner": "Platform Team",
   "owner_email": "platform@example.com",
   "disabled": false,
   "metadata": {
     "user": "12345"
   },
   "concurrency": "allow",
   "executor": "shell",
   "executor_config": {
     "command": "python3 /src/test_job.py"
   },
   "processors": {
     "log": {
       "forward": "true"
     }
   }
 }'

docker logs -f dkron
