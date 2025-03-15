# FilesToMarkdown Installation Guide

This guide will help you set up FilesToMarkdown without Docker.

## Prerequisites

- Ubuntu/Debian-based system
- Python 3.11+
- Node.js 18+
- PostgreSQL 16
- Redis
- MinIO

## Installation Steps

1. **Clone the repository and set up environment**
```bash
git clone [repository-url]
cd filestomarkdown
cp frontend/.env.example frontend/.env  # Create and edit with your settings
```

2. **Run the installation script**
```bash
cd backend/scripts
chmod +x install_dependencies.sh
./install_dependencies.sh
```

3. **Set up the database**
```bash
sudo -u postgres psql
CREATE DATABASE filestomarkdown;
CREATE USER filestomarkdown WITH PASSWORD 'your-secure-password';
ALTER ROLE filestomarkdown SET client_encoding TO 'utf8';
ALTER ROLE filestomarkdown SET default_transaction_isolation TO 'read committed';
ALTER ROLE filestomarkdown SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE filestomarkdown TO filestomarkdown;
\q

# Initialize the database
cd /opt/filestomarkdown/backend
source venv/bin/activate
alembic upgrade head
```

4. **Configure services**
```bash
# Copy service files
sudo cp backend/scripts/filestomarkdown.service /etc/systemd/system/
sudo cp backend/scripts/supervisor.conf /etc/supervisor/conf.d/

# Create system user
sudo useradd -m -r -s /bin/bash filestomarkdown
sudo chown -R filestomarkdown:filestomarkdown /opt/filestomarkdown

# Set up log directory
sudo mkdir -p /opt/filestomarkdown/logs
sudo chown -R filestomarkdown:filestomarkdown /opt/filestomarkdown/logs
```

5. **Build and deploy frontend**
```bash
cd frontend
npm install
npm run build

# Configure Nginx (example configuration)
sudo cp docker/nginx/nginx.conf /etc/nginx/sites-available/filestomarkdown
sudo ln -s /etc/nginx/sites-available/filestomarkdown /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Start services**
```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable filestomarkdown
sudo systemctl start filestomarkdown
sudo systemctl enable supervisor
sudo systemctl start supervisor

# Start all supervised programs
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

7. **Verify installation**
```bash
# Check service status
sudo systemctl status filestomarkdown
sudo supervisorctl status
```

The application should now be accessible at:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- MinIO Console: http://localhost:9001

## Environment Variables

Make sure to set the following environment variables in your `.env` file:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Database Configuration
POSTGRES_DB=filestomarkdown
POSTGRES_USER=filestomarkdown
POSTGRES_PASSWORD=your-secure-password

# MinIO Configuration
MINIO_ROOT_USER=your-minio-user
MINIO_ROOT_PASSWORD=your-minio-password
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Troubleshooting

1. **Service won't start**
- Check logs: `sudo journalctl -u filestomarkdown`
- Verify permissions: `ls -l /opt/filestomarkdown`
- Check Python environment: `source /opt/filestomarkdown/backend/venv/bin/activate`

2. **Database connection issues**
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection settings in `.env`
- Verify user permissions: `sudo -u postgres psql -c '\du'`

3. **MinIO errors**
- Check MinIO status: `sudo supervisorctl status minio`
- Verify storage permissions: `ls -l /opt/filestomarkdown/data/minio`
- Check MinIO logs: `tail -f /opt/filestomarkdown/logs/minio.err.log`

## Maintenance

1. **Backup database**
```bash
pg_dump -U filestomarkdown filestomarkdown > backup.sql
```

2. **Update application**
```bash
cd /opt/filestomarkdown
git pull
cd frontend && npm install && npm run build
cd ../backend && source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart filestomarkdown
sudo supervisorctl restart all
```

3. **View logs**
```bash
# Backend logs
tail -f /opt/filestomarkdown/logs/backend.out.log

# MinIO logs
tail -f /opt/filestomarkdown/logs/minio.out.log
