#!/bin/bash

# 📌 Exit immediately on error
set -e

# ✅ Load .env if it exists
if [ ! -f .env ]; then
  echo "❌ .env file not found! Please create one first."
  exit 1
fi

# 🧹 Clean up old standalone Docker objects (if run before compose)
echo "🧹 Cleaning up standalone containers and network..."
docker rm -f flask-frontend flask-backend mysql-db 2>/dev/null || true
docker network rm flask-API 2>/dev/null || true
docker rmi flask-frontend:1.0.0 flask-backend:1.0.0 2>/dev/null || true

# 🧹 Stop and remove all Compose services + volumes if already running
echo "🧹 Cleaning up existing Docker Compose services..."
docker compose --env-file .env down --volumes --remove-orphans

# 📁 Ensure log folder and file exist for backend bind mount
echo "📁 Creating logs directory and file for backend bind mount..."
mkdir -p ./backend/logs
touch ./backend/logs/output.txt

# 🐳 Build and start all services using Docker Compose
echo "🐳 Building and starting services with Docker Compose..."
docker compose --env-file .env up --build -d

echo "➡️ Please open http://localhost:800 manually in your browser"

# ✅ Done!
echo "✅ All services are up and running!"
echo "🌐 Frontend: http://localhost:800"
