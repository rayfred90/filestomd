#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Update package list and add PostgreSQL repository
sudo apt update
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    libpq-dev \
    pkg-config \
    libmagic1 \
    ffmpeg \
    poppler-utils \
    tesseract-ocr \
    ghostscript \
    postgresql-15 \
    postgresql-15-pgvector \
    postgresql-contrib \
    redis-server \
    supervisor \
    nginx \
    curl

# Start PostgreSQL service
sudo systemctl start postgresql

# Create python virtual environment
cd "$BACKEND_DIR"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Download and install MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/minio.deb -O minio.deb
sudo dpkg -i minio.deb
rm minio.deb

# Create necessary directories
sudo mkdir -p /opt/filestomarkdown/data/minio
sudo mkdir -p /opt/filestomarkdown/logs

# Enable pgvector extension
sudo -u postgres psql -c 'CREATE EXTENSION IF NOT EXISTS vector;'
