from typing import List
from uuid import UUID
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlmodel import Session, select

from ..models.file_model import File, FileResponse
from ..core.file_service import file_service, FileProcessingError, FileNotReadyError
from ..core.database import get_db

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile,
    db: Session = Depends(get_db)
) -> File:
    """Upload a file for processing."""
    try:
        return await file_service.process_file(file, db)
    except FileProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list", response_model=List[FileResponse])
async def list_files(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[File]:
    """List processed files with pagination."""
    statement = select(File).offset(skip).limit(limit)
    return db.exec(statement).all()

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: UUID,
    db: Session = Depends(get_db)
) -> File:
    """Get file information by ID."""
    file = db.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.get("/{file_id}/content")
async def get_file_content(
    file_id: UUID,
    content_type: str = "markdown"
) -> dict:
    """Get processed file content."""
    try:
        content, metadata = await file_service.get_file_content(file_id, content_type)
        return {
            "content": content,
            "metadata": metadata
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except FileNotReadyError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except FileProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{file_id}")
async def delete_file(
    file_id: UUID,
    db: Session = Depends(get_db)
) -> dict:
    """Delete a file and its processed content."""
    file = db.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from storage if paths exist
    if file.markdown_path:
        try:
            from ..core.storage import storage
            storage.delete_file(file.markdown_path)
            if file.json_path:
                storage.delete_file(file.json_path)
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Error deleting storage files: {e}")
    
    # Delete from database
    db.delete(file)
    db.commit()
    
    return {"status": "success", "message": "File deleted"}
