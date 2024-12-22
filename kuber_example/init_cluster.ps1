# Start Minikube
minikube start

# Set up Docker to use Minikube's Docker daemon
$env:DOCKER_TLS_VERIFY="1"
$env:DOCKER_HOST="tcp://$(minikube ip):2376"
$env:DOCKER_CERT_PATH="$(minikube ssh-key)"
$env:MINIKUBE_ACTIVE_DOCKERD="minikube"

# Build Docker images for backend and frontend
docker build -t simple-backend:latest .\backend
docker build -t simple-frontend:latest .\frontend

# Apply Kubernetes resources for Redis, Backend, and Frontend
kubectl apply -f k8s\redis-deployment.yaml
kubectl wait --for=condition=ready pod -l app=redis --timeout=300s

kubectl apply -f k8s\backend-deployment.yaml
kubectl apply -f k8s\backend-service.yaml
kubectl apply -f k8s\frontend-deployment.yaml
kubectl apply -f k8s\frontend-service.yaml

# Wait for the Backend and Frontend pods to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

# Open the frontend service in the browser
minikube service frontend-service

