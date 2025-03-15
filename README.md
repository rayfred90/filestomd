# Files to Markdown Converter

Convert various file types to markdown with embedded metadata, designed for accurate chunking and processing.

## Features

- Support for multiple file formats:
  - Documents: CSV, DOCX, EML, EPUB, HTML, MD, OST, PDF, PST, RST, RTF, SQL, TAR, TSV, TXT, XLS, MOBI
  - Images: JPG, PNG
  - Code files: Auto-detected by extension
- Embedded metadata in output files
- Position tracking for accurate content location
- JSON output with structured data
- Modern web interface with drag-and-drop
- Fast asynchronous processing
- Docker-based deployment

## Tech Stack

- **Frontend**:
  - Next.js 14 with App Router
  - React 19
  - TypeScript
  - Tailwind CSS 4
  - Shadcn UI
  - React Dropzone

- **Backend**:
  - FastAPI
  - SQLModel
  - PostgreSQL with pgvector
  - MinIO for file storage
  - Redis for caching
  - Various file processing libraries

## Project Structure

```
filestomarkdown/
├── frontend/           # Next.js frontend application
├── backend/           # FastAPI backend application
├── db/               # Database migrations and init scripts
├── routers/          # API route handlers
└── docker/           # Docker configuration files
```

## Setup

1. **Prerequisites**:
   - Docker and Docker Compose
   - Node.js 20+ (for local development)
   - Python 3.11+ (for local development)

2. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   # PostgreSQL
   POSTGRES_DB=filestomarkdown
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=your_password

   # MinIO
   MINIO_ROOT_USER=minioadmin
   MINIO_ROOT_PASSWORD=minioadmin
   ```

3. **Docker Setup**:
   ```bash
   # Build and start services
   docker-compose up --build
   ```

4. **Local Development Setup**:
   ```bash
   # Frontend
   cd frontend
   npm install
   npm run dev

   # Backend
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

## Usage

1. Access the web interface at `http://localhost:3000`
2. Drag and drop files or use the file picker
3. Files will be processed and converted to markdown/JSON
4. Download or view the converted files
5. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `POST /api/v1/files/upload` - Upload file for processing
- `GET /api/v1/files/list` - List processed files
- `GET /api/v1/files/{file_id}` - Get file information
- `GET /api/v1/files/{file_id}/content` - Get processed content
- `DELETE /api/v1/files/{file_id}` - Delete file and its content

## Output Format

### Markdown Output
```markdown
---
title: Document Title
author: Author Name
date: Creation Date
page_count: 5
word_count: 1000
...other metadata
---

Document content with preserved formatting...
```

### JSON Output
```json
{
  "content": "Document content...",
  "metadata": {
    "title": "Document Title",
    "positions": [
      {
        "page": 1,
        "x": 100,
        "y": 200,
        "content": "Text snippet"
      }
    ]
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Create Pull Request

## License

MIT License - see LICENSE file for details
# filestomarkdown
