#!/bin/bash

echo "🚀 Starting Minikube..."
minikube start

echo "📦 Applying K8s Manifests..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/prometheus-service.yaml
kubectl apply -f k8s/grafana-deployment.yaml
kubectl apply -f k8s/grafana-service.yaml

echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=resource-monitor --timeout=90s
kubectl wait --for=condition=ready pod -l app=prometheus --timeout=90s
kubectl wait --for=condition=ready pod -l app=grafana --timeout=90s

echo "🌐 Launching Grafana and Prometheus..."
minikube service prometheus-service &
minikube service grafana-service &

echo "✅ Done! Everything is running. You can log in to Grafana with admin/admin."