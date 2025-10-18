#!/bin/bash

# Verity AI Kubernetes Deployment Script

set -e

echo "🚀 Deploying Verity AI to Kubernetes..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if we're connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Not connected to a Kubernetes cluster"
    exit 1
fi

echo "✅ Connected to cluster: $(kubectl config current-context)"

# Navigate to k8s directory
cd "$(dirname "$0")"

# Create namespace (optional)
echo "📁 Creating namespace..."
kubectl apply -f k8s-namespace.yaml

# Apply ConfigMap
echo "⚙️  Applying ConfigMap..."
kubectl apply -f k8s-configmap.yaml

# Apply Secret (you need to update the API key first!)
echo "🔐 Applying Secrets..."
echo "⚠️  WARNING: Update the OpenAI API key in k8s-secret.yaml before deploying!"
read -p "Have you updated the OpenAI API key in k8s-secret.yaml? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please update the OpenAI API key in k8s-secret.yaml first"
    echo "   You can encode your key with: echo -n 'your-key' | base64"
    exit 1
fi
kubectl apply -f k8s-secret.yaml

# Apply Deployment
echo "🚀 Deploying application..."
kubectl apply -f k8s-deployment.yaml

# Apply Service
echo "🌐 Creating services..."
kubectl apply -f k8s-service.yaml

# Apply HPA
echo "📊 Setting up autoscaling..."
kubectl apply -f k8s-hpa.yaml

# Optional: Apply Ingress (uncomment if you have an ingress controller)
# echo "🌍 Setting up ingress..."
# kubectl apply -f k8s-ingress.yaml

echo "✅ Deployment complete!"
echo ""
echo "📋 Useful commands:"
echo "   Check pods:        kubectl get pods -l app=verity-ai"
echo "   Check services:    kubectl get svc -l app=verity-ai"
echo "   Check logs:        kubectl logs -l app=verity-ai -f"
echo "   Port forward:      kubectl port-forward svc/verity-ai-service 8080:80"
echo "   Scale deployment:  kubectl scale deployment verity-ai-deployment --replicas=5"
echo "   Delete all:        kubectl delete -f ."
echo ""
echo "🌐 Access your app:"
echo "   NodePort:          http://your-cluster-ip:30060"
echo "   Port Forward:      http://localhost:8080 (after port-forward command)"

# Wait for deployment to be ready
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/verity-ai-deployment

echo "🎉 Verity AI is now running on Kubernetes!"