# Verity AI - Kubernetes Deployment

This directory contains all the Kubernetes manifests and deployment scripts for Verity AI.

## 📁 Files Overview

### **Core Kubernetes Manifests:**
- `k8s-deployment.yaml` - Main application deployment with 2 replicas
- `k8s-service.yaml` - ClusterIP and NodePort services
- `k8s-secret.yaml` - Secrets for OpenAI API key
- `k8s-configmap.yaml` - Configuration for environment variables
- `k8s-namespace.yaml` - Optional dedicated namespace
- `k8s-hpa.yaml` - Horizontal Pod Autoscaler (2-10 replicas)
- `k8s-ingress.yaml` - Ingress for external access (requires ingress controller)

### **Deployment Tools:**
- `deploy-k8s.sh` - Automated deployment script
- `kustomization.yaml` - Kustomize configuration for GitOps

## 🚀 Quick Deployment

### **1. Prerequisites**
```bash
# Ensure kubectl is installed and connected
kubectl cluster-info
```

### **2. Update Secrets**
Before deploying, update your OpenAI API key:
```bash
# Encode your API key
echo -n "your-actual-openai-api-key" | base64

# Edit k8s-secret.yaml and replace the encoded value
```

### **3. Deploy**
```bash
# Run the deployment script
./deploy-k8s.sh

# OR deploy manually
kubectl apply -f .
```

### **4. Access Your Application**
```bash
# Via NodePort (external access)
http://your-cluster-ip:30060

# Via Port Forward (local development)
kubectl port-forward svc/verity-ai-service 8080:80
# Then access: http://localhost:8080
```

## 📊 Monitoring & Management

### **Check Status**
```bash
# Check pods
kubectl get pods -l app=verity-ai

# Check services
kubectl get svc -l app=verity-ai

# Check autoscaling
kubectl get hpa verity-ai-hpa

# View logs
kubectl logs -l app=verity-ai -f
```

### **Scaling**
```bash
# Manual scaling
kubectl scale deployment verity-ai-deployment --replicas=5

# Auto-scaling is configured (2-10 replicas based on CPU/memory)
```

### **Health Checks**
```bash
# Test health endpoint
kubectl exec -it deployment/verity-ai-deployment -- curl localhost:6000/health
```

## 🔧 Configuration

### **Environment Variables (ConfigMap)**
- `MODEL_PATH`: Path to ML model file
- `PORT`: Application port (6000)
- `FLASK_DEBUG`: Debug mode (false for production)
- `GUNICORN_WORKERS`: Number of worker processes
- `GUNICORN_TIMEOUT`: Request timeout

### **Secrets**
- `OPENAI_API_KEY`: OpenAI API key for LLM functionality

### **Resource Limits**
- **Requests**: 250m CPU, 512Mi memory
- **Limits**: 500m CPU, 1Gi memory
- **Auto-scaling**: 70% CPU, 80% memory thresholds

## 🌐 API Endpoints

Once deployed, your API will be available at:
- `GET /health` - Health check
- `POST /predict` - ML predictions
- `POST /maintenance-advice` - AI-powered maintenance advice

## 🗑️ Cleanup

```bash
# Remove all resources
kubectl delete -f .

# Or use labels
kubectl delete all -l app=verity-ai
```

## 🎯 Production Considerations

1. **Ingress**: Configure ingress controller and update `k8s-ingress.yaml` with your domain
2. **TLS**: Set up cert-manager for automatic SSL certificates
3. **Monitoring**: Add Prometheus/Grafana monitoring
4. **Logging**: Configure centralized logging (ELK stack, Fluentd)
5. **Security**: Network policies, pod security standards
6. **Backup**: Regular backup of model files and configurations

## 🔄 GitOps with Kustomize

```bash
# Deploy using Kustomize
kubectl apply -k .

# Or with custom overlays
kubectl apply -k overlays/production
```