# To-Do App Kubernetes Deployment

This project documents the Kubernetes deployment of a To-Do web application. It consists of a Flask-based backend with a SQLite database and a frontend served using Nginx. Both components are containerized and deployed to a Google Kubernetes Engine (GKE) cluster using YAML manifests, with support for autoscaling, ingress, and persistent volumes.

---

## 1. Application and Dependencies

### Application Components

- **Backend:** Flask REST API with SQLite database for storing tasks.
- **Frontend:** Static React-like UI served with Nginx.

### Dependencies

- Flask (backend routing)
- SQLite (task storage)
- Nginx (serving frontend files)

Since the backend uses a local SQLite database, a PersistentVolumeClaim (PVC) is used to ensure that database data persists across pod restarts.

---

## 2. Docker Image Building and Pushing

We containerized both the frontend and backend applications, then pushed the Docker images to DockerHub so Kubernetes could pull them.

### Clone the GitHub Repository

Before building, clone the project repository locally:

```bash
git clone https://github.com/marybarbiebarrion/Grp-2-Barrion-DeGuzman-Medina-Pitogo.git
cd Grp-2-Barrion-DeGuzman-Medina-Pitogo
```

We also logged in to DockerHub via the console to authenticate:

```bash
docker login adriandeguzman
```
**Backend:**
```bash
docker build -t adriandeguzman/todo-backend:latest ./backend
docker push adriandeguzman/todo-backend:latest
```

**Frontend:**
```bash
docker build -t adriandeguzman/todo-frontend:latest ./frontend
docker push adriandeguzman/todo-frontend:latest
```

---

## 3. Kubernetes Cluster Deployment

We used Google Cloud Platform (GCP) to create a standard (non-private) Kubernetes cluster with 2 nodes.
Instead of using the command line to create the cluster, we manually set it up using the GCP Console:

- In the Navigation menu, go to Kubernetes Engine > Clusters.
- Click Create and then select Switch to Standard Cluster.
-Name the cluster todo-cluster.
- Set the Location Type to Zone, and choose a zone which was us-central1-a.
- In the left pane, under Node Pools, click default-pool and set Number of nodes to 2.
- In the left pane, under Cluster, click Networking, and ensure the cluster is not set to private.

We specifically avoided a private cluster because it caused issues during deployment. When we tried using a private cluster, kubectl apply commands would hang or show no output. Based on research, this happened because private clusters restrict direct access to the control plane. Without setting up extra networking configurations (like a bastion host or VPN), manifests could not be applied from Cloud Shell. To bypass this limitation and keep the setup simple, we created a standard (public) cluster instead.

After creating the cluster, we configured kubectl to connect to it from Cloud Shell:


```bash
gcloud config set project grp2-containers
gcloud config set compute/zone us-central1-c
gcloud container clusters get-credentials todo-cluster
```
This allowed us to deploy all resources to the cluster using kubectl from the terminal.

---

## 4. Applying Manifests

All Kubernetes manifest files are located in the kubernetes-manifests/ folder. To deploy everything, we ran:

```bash
kubectl apply -f kubernetes-manifests/
```

This command creates all necessary resources including:
- **Deployments:** backend-deployment.yaml, frontend-deployment.yaml — define pods for backend and frontend.
- **Persistent Volume Claim:** backend-pvc.yaml — ensures storage persistence for the backend’s SQLite database.
- **Services:** backend-service.yaml, frontend-service.yaml — expose pods internally within the cluster.
- **Horizontal Pod Autoscalers:** hpa-backend.yaml, hpa-frontend.yaml — automatically scale pods based on CPU usage.
- **Ingress:** ingress.yaml — exposes the frontend externally via HTTP without using a LoadBalancer service.

**How the manifests were created**
Initially, I used example manifests from trusted Kubernetes tutorials and official docs as templates. Then, I customized them to fit the project:
- Deployment manifests were tailored to specify the correct Docker images from DockerHub and mount the persistent volume for the backend.
- The PVC manifest was set to request storage for the SQLite file based on the backend’s needs.
- Services were created as ClusterIP type to allow internal communication and ingress routing.
- Autoscaler manifests set CPU target thresholds and maximum pod counts based on typical workload.
- The ingress manifest routes external HTTP traffic to the frontend service, complying with project requirements (no LoadBalancer service).

While I started by copy-pasting these templates, we made sure to adjust each resource for our app’s architecture and requirements.

---

## 5. Pods

We used Deployment resources to manage pods for both components:

- **Backend** and **frontend** pods are deployed and managed by Deployments.
- **Backend Pod** mounts a PersistentVolumeClaim at /app for SQLite storage.
- **Frontend Pod** serves static files using Nginx.

To view pod status, we use:

```bash
kubectl get pods
```

To debug, we use:
```bash
kubectl describe pod $(kubectl get pods | grep backend | awk ‘{print$1}’)
```

---

## 6. Services

Backend and frontend services use **ClusterIP** for internal communication within the cluster.

- **backend-service**: Port **5000** → **Backend Pod**
- **frontend-service**: Port **80** → **Frontend Pod**

To verify the services, we run:

```bash
kubectl get services
```

---

## 7. Ingress

We configured an Ingress to expose the frontend publicly without using a LoadBalancer. It routes HTTP traffic on port 80 to the frontend-service.

The frontend communicates internally with the backend using the backend service name.

- **No LoadBalancer service is used** to expose the app, relying solely on Ingress for external access.

To check the ingress and get the external address, run:

```bash
kubectl get ingress
```

The external IP address appears under the **ADDRESS** column. We used this address as the app URL, for example:

34.117.185.16

Therefore, Our application is accessible at the following **IP address**:

  
  **http://34.117.185.167/**

---

## 8. Autoscaling

We used HorizontalPodAutoscaler (HPA) for both frontend and backend:

- HPA are configured for both backend and frontend deployments.
- Target CPU usage: 50%
- Minimum pods: 1
- Maximum pods: 5

To check the autoscaling status, run:

```bash
kubectl get hpa
```

---

## 9. Storage Persistence

The backend pod uses a PersistentVolumeClaim named backend-pvc:

- Mounted at /app, where the SQLite DB is located.
- Provisioned automatically when PVC is applied.
- Survives pod restarts and deletions.

To check storage, we use:

```bash
kubectl get pvc
```

---

## Live App

**URL:** [http://34.117.185.167/](http://34.117.185.167/)

> All Kubernetes YAML configuration files are located in the [`/kubernetes-manifests`](./kubernetes-manifests) directory.
