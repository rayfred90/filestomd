#!/bin/bash

# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    build-essential \
    libpq-dev \
    pkg-config \
    libmagic1 \
    ffmpeg \
    poppler-utils \
    tesseract-ocr \
    ghostscript \
    postgresql \
    postgresql-contrib \
    redis-server \
    supervisor \
    nginx \
    curl

# Create python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Download and install MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20240315234217.0.0_amd64.deb -O minio.deb
sudo dpkg -i minio.deb
rm minio.deb

# Create necessary directories
sudo mkdir -p /opt/filestomarkdown/data/minio
sudo mkdir -p /opt/filestomarkdown/logs
