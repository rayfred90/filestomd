#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Update package list and add PostgreSQL repository (using new key method)
sudo apt update
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt update

# Install system dependencies for unstructured and other packages
sudo apt install -y \
    python3-full \
    python3-venv \
    build-essential \
    libpq-dev \
    pkg-config \
    libmagic1 \
    ffmpeg \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-all \
    ghostscript \
    postgresql-17 \
    postgresql-server-dev-17 \
    redis-server \
    supervisor \
    nginx \
    curl \
    git \
    libreoffice \
    pandoc \
    libmagic-dev

# Install pgvector from source
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
cd ..
rm -rf pgvector

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create python virtual environment
cd "$BACKEND_DIR"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Download and install MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/minio.deb -O minio.deb
sudo dpkg -i minio.deb
rm minio.deb

# Create necessary directories
sudo mkdir -p /opt/filestomarkdown/data/minio
sudo mkdir -p /opt/filestomarkdown/logs

# Enable pgvector extension and create database
sudo -u postgres psql <<EOF
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'filestomarkdown') THEN
        CREATE DATABASE filestomarkdown;
    END IF;
END
\$\$;
\c filestomarkdown
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_extension WHERE extname = 'vector'
    ) THEN
        CREATE EXTENSION IF NOT EXISTS vector;
    END IF;
END
\$\$;
EOF

# Restart PostgreSQL to ensure pgvector is properly loaded
sudo systemctl restart postgresql
