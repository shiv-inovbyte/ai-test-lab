#!/bin/bash

# Verity AI Kubernetes Cleanup Script

set -e

echo "🗑️  Cleaning up Verity AI from Kubernetes..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Navigate to k8s directory
cd "$(dirname "$0")"

echo "📋 Current Verity AI resources:"
kubectl get all -l app=verity-ai

echo ""
read -p "🤔 Are you sure you want to delete all Verity AI resources? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

echo "🗑️  Deleting resources..."

# Delete all resources in order
kubectl delete -f k8s-hpa.yaml --ignore-not-found=true
kubectl delete -f k8s-ingress.yaml --ignore-not-found=true
kubectl delete -f k8s-service.yaml --ignore-not-found=true
kubectl delete -f k8s-deployment.yaml --ignore-not-found=true
kubectl delete -f k8s-secret.yaml --ignore-not-found=true
kubectl delete -f k8s-configmap.yaml --ignore-not-found=true
# kubectl delete -f k8s-namespace.yaml --ignore-not-found=true  # Uncomment if you want to delete namespace

echo "✅ Cleanup complete!"
echo "📊 Remaining resources (should be empty):"
kubectl get all -l app=verity-ai