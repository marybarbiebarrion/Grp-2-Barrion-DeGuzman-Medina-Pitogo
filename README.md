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

Frontend (Web Interface): [http://localhost:8080](http://localhost:8080)
Backend (Flask API): [http://localhost:5000](http://localhost:5000)

---

## How to Stop the Application

To stop the running containers, press CTRL + C in the terminal.
To remove all running containers and clean up:

docker-compose down
