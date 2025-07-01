#!/bin/bash

# Clean up any existing containers and network
docker rm -f flask-frontend flask-backend 2>/dev/null
docker network rm flask-API 2>/dev/null
docker rmi flask-frontend:1.0.0 flask-backend:1.0.0 2>/dev/null

# Prepare logs directory and file on the host
mkdir -p "./backend/logs"
touch "./backend/logs/output.txt"

# Create Docker network for frontend-backend communication
docker network create flask-API

# Build backend image
docker build -t flask-backend:1.0.0 ./backend

# Build frontend image
docker build -t flask-frontend:1.0.0 ./frontend

# Run backend container with proper bind-mount path
docker run -d --name flask-backend \
    --network flask-API \
    -v "$(pwd)/backend/logs/output.txt:/app/flaskAPI/logs/output.txt" \
    flask-backend:1.0.0

# Run frontend container with port exposed to host
docker run -d --name flask-frontend \
    -p 800:80 \
    --network flask-API \
    flask-frontend:1.0.0
