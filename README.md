# Files to Markdown Converter

Convert various file formats to markdown with embedded metadata, designed for accurate chunking and processing.

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

## Tech Stack

- **Frontend**:
  - Next.js 14 with App Router
  - React 19
  - TypeScript
  - Tailwind CSS 4
  - Shadcn UI
  - React Dropzone

- **Backend**:
  - FastAPI 0.115.11
  - Python 3.12
  - PostgreSQL 17 with pgvector
  - MinIO for file storage
  - Redis for caching

## Project Structure

```
/opt/filestomarkdown/filestomd/
├── frontend/           # Next.js frontend application
│   ├── app/          # Next.js app directory
│   ├── components/   # React components
│   └── lib/         # Utility functions and types
├── backend/           # FastAPI backend application
│   ├── app/          # Application modules
│   │   ├── core/    # Core functionality
│   │   ├── models/  # Database models
│   │   ├── routers/ # API endpoints
│   │   └── utils/   # Utility functions
│   └── scripts/     # Installation and setup scripts
└── db/              # Database migrations and init scripts
```

## Installation

For bare metal installation on Ubuntu 24.04:
1. Install python3-full and other prerequisites
2. Follow the detailed instructions in [INSTALL.md](INSTALL.md)

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
