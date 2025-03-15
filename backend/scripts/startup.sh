#!/bin/bash

# Source the virtual environment
source venv/bin/activate

# Wait for MinIO to be ready
echo "Waiting for MinIO to be ready..."
until curl --silent --fail http://localhost:9000/minio/health/live; do
    echo "MinIO is not ready - waiting..."
    sleep 5
done

echo "MinIO is ready - initializing buckets..."

# Initialize MinIO buckets
python scripts/init-minio.py

echo "MinIO initialization complete"

# Start the FastAPI application using supervisor
echo "Starting services using supervisor..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all

echo "Services started successfully. Check supervisor status with: supervisorctl status"
