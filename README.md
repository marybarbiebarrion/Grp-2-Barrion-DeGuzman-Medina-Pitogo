# iscs-docker-multicon-app

## To-Do List Full Stack Application (Dockerized)

This project is a simple full-stack To-Do List web application with a Flask backend and a static frontend (HTML/CSS/JavaScript), containerized using Docker.

---

## Prerequisites

Ensure that Docker is installed on your system:

- Download Docker from the official site: [https://www.docker.com/](https://www.docker.com/)

**For Windows:** Choose the installer for Windows (amd64)  
**For macOS:** Select the appropriate version based on your Mac's architecture (Apple Silicon or Intel)

---

## How to Run

### Build and Start the Application

In the root directory (where `docker-compose.yml` is located), run:

docker-compose up --build

### Access the Application

- Frontend (Web Interface): [http://localhost:8080](http://localhost:8080)
- Backend (Flask API): [http://localhost:5000](http://localhost:5000)

---

## How to Stop the Application

To stop the running containers, press CTRL + C in the terminal.
To remove all running containers and clean up:

docker-compose down



---

# To-Do App Kubernetes Deployment

This document explains how to deploy the To-Do application on Kubernetes, covering the entire process from Docker image building to creating Kubernetes resources.

---

## 1. Application and Dependencies

- **Backend**: Flask API with SQLite database  
- **Frontend**: React-like app served with Nginx  
- Backend depends on persistent storage (SQLite DB) via PersistentVolumeClaim (PVC).

---

## 2. Docker Image Building and Pushing

Build and push Docker images to DockerHub so Kubernetes can pull them:

```bash
# Build backend image
docker build -t adriandeguzman/todo-backend:latest ./backend
docker push adriandeguzman/todo-backend:latest

# Build frontend image
docker build -t adriandeguzman/todo-frontend:latest ./frontend
docker push adriandeguzman/todo-frontend:latest

---

## 3. Kubernetes Cluster Deployment

- Create a Kubernetes cluster (e.g., using Google Cloud).
- Clone your repository and ensure your Kubernetes manifests are located in the `kubernetes-manifests/` folder.
- Apply the manifests with the following command:

```bash
kubectl apply -f kubernetes-manifests/

---

## 4. Pods

- Backend and frontend pods are deployed and managed by Deployments.
- Backend pod mounts the PersistentVolumeClaim (PVC) for persistent SQLite storage.

Check pod status with:

```bash
kubectl get pods


---

## 5. Services

Backend and frontend services use **ClusterIP** for internal communication within the cluster.

- **Backend service** exposes port **5000**  
- **Frontend service** exposes port **80**

To verify the services, run:

```bash
kubectl get services

---

## 6. Ingress

- Ingress exposes the **frontend application externally on port 80**.
- **No LoadBalancer service is used** to expose the app, relying solely on Ingress for external access.
- **IMPORTANT:** Your application is accessible at the **following IP address**:

  
  👉 **http://34.117.185.167/** 👈

- To verify or get the current Ingress IP, run:

```bash
kubectl get ingress

---

## 7. Autoscaling

- Horizontal Pod Autoscalers (HPA) are configured for both backend and frontend deployments.
- Pods automatically scale based on CPU usage, targeting 50% CPU utilization.
- To check the autoscaling status, run:

```bash
kubectl get hpa

---

## 8. Storage Persistence

- The backend uses a PersistentVolumeClaim named `backend-pvc`.
- This PVC ensures that the SQLite database files persist across pod restarts, maintaining data durability.

