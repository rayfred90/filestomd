from typing import Dict, Any, Tuple, Optional
from pathlib import Path
import os
import uuid
from datetime import datetime

from sqlmodel import Session
from fastapi import UploadFile

from ..models.file_model import File, FileStatus
from ..processors.factory import ProcessorFactory, UnsupportedFileType
from .storage import storage, StorageError
from .database import get_session

class FileService:
    """Service for handling file processing and storage operations."""
    
    def __init__(self, upload_folder: str = "uploads"):
        self.upload_folder = Path(upload_folder)
        self.upload_folder.mkdir(exist_ok=True)

    async def process_file(self, file: UploadFile, db: Session) -> File:
        """
        Process an uploaded file, converting it to markdown and JSON.
        
        Args:
            file: The uploaded file
            db: Database session
            
        Returns:
            File model instance with processing results
        """
        try:
            # Create temporary file path
            temp_path = self.upload_folder / f"{uuid.uuid4()}_{file.filename}"
            
            # Save uploaded file
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Create file record
            file_record = File(
                filename=file.filename,
                original_type=file.content_type or "",
                file_size=os.path.getsize(temp_path),
                status=FileStatus.PROCESSING
            )
            db.add(file_record)
            db.commit()
            
            try:
                # Get processor for file type
                processor = ProcessorFactory.create_processor(temp_path, file_record)
                
                # Process file
                markdown, json_content, metadata = await processor.process()
                
                # Save results to storage
                file_id = str(file_record.id)
                
                # Save original file
                orig_path = f"{file_id}/original/{file.filename}"
                storage.save_file(temp_path, orig_path, file.content_type)
                
                # Save markdown
                md_path = f"{file_id}/markdown/{Path(file.filename).stem}.md"
                storage.save_content(markdown, md_path, "text/markdown")
                
                # Save JSON
                json_path = f"{file_id}/json/{Path(file.filename).stem}.json"
                storage.save_json(json_content, json_path)
                
                # Update file record
                file_record.status = FileStatus.COMPLETED
                file_record.metadata = metadata
                file_record.markdown_path = md_path
                file_record.json_path = json_path
                file_record.page_count = metadata.get("page_count")
                file_record.word_count = len(markdown.split())
                file_record.chunk_count = len(metadata.get("positions", []))
                
            except (UnsupportedFileType, StorageError) as e:
                file_record.status = FileStatus.FAILED
                file_record.error_message = str(e)
                raise
                
            finally:
                # Clean up temporary file
                if temp_path.exists():
                    temp_path.unlink()
                
                db.commit()
            
            return file_record
            
        except Exception as e:
            raise FileProcessingError(f"Error processing file: {str(e)}")

    async def get_file_content(
        self,
        file_id: uuid.UUID,
        content_type: str = "markdown"
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Retrieve processed file content.
        
        Args:
            file_id: ID of the file to retrieve
            content_type: Type of content to retrieve ('markdown' or 'json')
            
        Returns:
            Tuple of (content, metadata)
        """
        with get_session() as db:
            file_record = db.get(File, file_id)
            if not file_record:
                raise FileNotFoundError(f"File not found: {file_id}")
            
            if file_record.status != FileStatus.COMPLETED:
                raise FileNotReadyError(
                    f"File not ready. Status: {file_record.status}"
                )
            
            try:
                if content_type == "markdown":
                    content = storage.get_file(file_record.markdown_path).decode()
                else:  # json
                    content = storage.get_json(file_record.json_path)
                
                return content, file_record.metadata
                
            except StorageError as e:
                raise FileProcessingError(f"Error retrieving file: {str(e)}")

class FileProcessingError(Exception):
    """Raised when there's an error processing a file."""
    pass

class FileNotReadyError(Exception):
    """Raised when trying to access a file that's not finished processing."""
    pass

# Create singleton instance
file_service = FileService()
