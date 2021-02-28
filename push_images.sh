#!/bin/bash

docker build -t eu.gcr.io/kubernetes-labs-293308/admin-server -f admin_api/Dockerfile ./admin_api
docker build -t eu.gcr.io/kubernetes-labs-293308/worker -f worker/Dockerfile ./worker
docker build -t eu.gcr.io/kubernetes-labs-293308/primer -f primer/Dockerfile ./primer

docker push eu.gcr.io/kubernetes-labs-293308/admin-server
docker push eu.gcr.io/kubernetes-labs-293308/worker
docker push eu.gcr.io/kubernetes-labs-293308/primer
