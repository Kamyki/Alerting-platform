#!/bin/bash
set -e

#gcloud container clusters create lab-cluster --zone us-central1-c --num-nodes 5 --scopes "https://www.googleapis.com/auth/cloud-platform"

docker build -t eu.gcr.io/kubernetes-labs-293308/admin-server -f admin_api/Dockerfile ./admin_api
docker build -t eu.gcr.io/kubernetes-labs-293308/worker -f worker/Dockerfile ./worker
docker build -t eu.gcr.io/kubernetes-labs-293308/primer -f primer/Dockerfile ./primer

docker push eu.gcr.io/kubernetes-labs-293308/admin-server
docker push eu.gcr.io/kubernetes-labs-293308/worker
docker push eu.gcr.io/kubernetes-labs-293308/primer

kubectl delete -f  kubernetes/role.yml
kubectl delete -f  kubernetes/dkron-server-statefulset.yml
kubectl delete -f  kubernetes/configmap.yml
kubectl delete -f  kubernetes/secret.yml
kubectl delete -f  kubernetes/dkron-worker-agent-deployment.yml
kubectl delete -f  kubernetes/admin-server-deployment.yml
kubectl delete -f  kubernetes/primer-job.yml
kubectl delete pod --all

kubectl apply -f  kubernetes/role.yml
kubectl apply -f  kubernetes/configmap.yml
kubectl apply -f  kubernetes/secret.yml
kubectl apply -f  kubernetes/dkron-server-statefulset.yml

sleep 30 # let servers initialize

kubectl apply -f  kubernetes/dkron-worker-agent-deployment.yml
kubectl apply -f  kubernetes/admin-server-deployment.yml
kubectl apply -f  kubernetes/primer-job.yml
