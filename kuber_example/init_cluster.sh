#!/bin/bash
minikube start
eval $(minikube docker-env)

docker build -t simple-backend:latest ./backend
docker build -t simple-frontend:latest ./frontend

kubectl apply -f k8s/redis-deployment.yaml
kubectl wait --for=condition=ready pod -l app=redis --timeout=300s

kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

minikube service frontend-service