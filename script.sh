#!/bin/bash

# Clean up
docker rm -f flask-frontend flask-backend 2>/dev/null
docker network rm flask-API 2>/dev/null
docker rmi flask-frontend:1.0.0 flask-backend:1.0.0 2>/dev/null
docker volume rm logs-volume 2>/dev/null

# Create Docker volume
docker volume create logs-volume

# Create network
docker network create flask-API

# Build backend
docker build -t flask-backend:1.0.0 ./backend

# Build frontend
docker build -t flask-frontend:1.0.0 ./frontend

# Run backend (NO port exposed — only network!)
docker run -d --name flask-backend --network flask-API -v logs-volume:/app/flaskAPI/logs flask-backend:1.0.0

# Run frontend (port 800 exposed)
docker run -d --name flask-frontend -p 800:80 --network flask-API flask-frontend:1.0.0