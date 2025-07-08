#!/bin/bash

# ✅ Load environment variables from .env for use in this script
set -a
source .env
set +a

echo "🧹 Cleaning up old containers and network..."
docker rm -f flask-frontend flask-backend mysql-db 2>/dev/null
docker network rm flask-API 2>/dev/null
docker rmi flask-frontend:1.0.0 flask-backend:1.0.0 2>/dev/null

echo "📁 Preparing logs directory..."
mkdir -p "./backend/logs"
touch "./backend/logs/output.txt"

echo "🌐 Creating Docker network..."
docker network create flask-API

echo "🐳 Starting MySQL container..."
docker run -d --name mysql-db \
  --network flask-API \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
  -e MYSQL_DATABASE="$DB_NAME" \
  -e MYSQL_USER="$DB_USER" \
  -e MYSQL_PASSWORD="$DB_PASSWORD" \
  -v mysql-data:/var/lib/mysql \
  mysql:8

echo "🐳 Building backend image..."
docker build --no-cache -t flask-backend:1.0.0 ./backend

echo "🚀 Running backend container..."
docker run -d --name flask-backend \
  --network flask-API \
  -v "$(pwd)/backend/logs:/app/flaskAPI/logs" \
  --env-file .env \
  flask-backend:1.0.0
    
echo "🌐 Building frontend image..."
docker build --no-cache -t flask-frontend:1.0.0 ./frontend

echo "🚀 Running frontend container..."
docker run -d --name flask-frontend \
  -p 800:80 \
  --network flask-API \
  flask-frontend:1.0.0

echo "✅ All containers are up!"
