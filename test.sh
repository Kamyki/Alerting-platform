docker stop $(docker ps -q)

cp ./worker/mongo.py ./primer/mongo.py
cp ./worker/mongo.py ./admin_api/mongo.py
cp ./worker/utils.py ./primer/utils.py
cp ./worker/utils.py ./admin_api/utils.py



docker build -t alerting-platform/admin-server -f admin_api/Dockerfile ./admin_api
docker build -t alerting-platform/worker -f worker/Dockerfile ./worker

docker run -p 8080:8080  --name dkron --rm -d alerting-platform/worker \
  agent --server --bootstrap-expect=1 --config /app/dkron.yml

docker run -p 80:80 -p 27017:27017 --rm --name admin-server -d alerting-platform/admin-server

echo "Docker is up"

cd ./admin_api ; ./run_tests.sh ; cd ..

cd ./primer ; python3 primer.py ; cd ..

docker logs -f dkron
