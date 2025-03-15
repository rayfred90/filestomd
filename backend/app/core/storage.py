from minio import Minio
from minio.error import S3Error
from typing import Optional, BinaryIO
from pathlib import Path
import json
from .config import settings

class StorageService:
    """Service for handling file storage operations using MinIO."""
    
    def __init__(self):
        self.client = Minio(
            f"{settings.MINIO_HOST}:{settings.MINIO_PORT}",
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=False  # Set to True if using HTTPS
        )
        self.bucket_name = settings.MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the storage bucket exists, create if it doesn't."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise StorageError(f"Failed to initialize storage bucket: {str(e)}")

    def save_file(
        self,
        file_path: str | Path,
        object_name: str,
        content_type: Optional[str] = None
    ) -> str:
        """
        Save a file to storage.
        
        Args:
            file_path: Path to the file to upload
            object_name: Name to save the file as in storage
            content_type: Optional MIME type of the file
            
        Returns:
            The object name/path in storage
        """
        try:
            self.client.fput_object(
                self.bucket_name,
                object_name,
                str(file_path),
                content_type=content_type
            )
            return object_name
        except S3Error as e:
            raise StorageError(f"Failed to save file: {str(e)}")

    def save_content(
        self,
        content: str | bytes | BinaryIO,
        object_name: str,
        content_type: Optional[str] = None
    ) -> str:
        """
        Save content directly to storage.
        
        Args:
            content: The content to save
            object_name: Name to save the content as in storage
            content_type: Optional MIME type of the content
            
        Returns:
            The object name/path in storage
        """
        try:
            # Convert string content to bytes if needed
            if isinstance(content, str):
                content = content.encode('utf-8')
            
            # Convert bytes to file-like object if needed
            if isinstance(content, bytes):
                from io import BytesIO
                content = BytesIO(content)
            
            # Get content length
            content.seek(0, 2)  # Seek to end
            content_length = content.tell()
            content.seek(0)  # Reset to beginning
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                content,
                content_length,
                content_type=content_type
            )
            return object_name
        except S3Error as e:
            raise StorageError(f"Failed to save content: {str(e)}")

    def save_json(self, data: dict, object_name: str) -> str:
        """
        Save JSON data to storage.
        
        Args:
            data: The JSON data to save
            object_name: Name to save the JSON as in storage
            
        Returns:
            The object name/path in storage
        """
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            return self.save_content(
                json_str,
                object_name,
                content_type="application/json"
            )
        except Exception as e:
            raise StorageError(f"Failed to save JSON: {str(e)}")

    def get_file(self, object_name: str) -> bytes:
        """
        Retrieve a file from storage.
        
        Args:
            object_name: Name of the file in storage
            
        Returns:
            The file contents as bytes
        """
        try:
            response = self.client.get_object(
                self.bucket_name,
                object_name
            )
            return response.read()
        except S3Error as e:
            raise StorageError(f"Failed to retrieve file: {str(e)}")
        finally:
            if 'response' in locals():
                response.close()
                response.release_conn()

    def get_json(self, object_name: str) -> dict:
        """
        Retrieve JSON data from storage.
        
        Args:
            object_name: Name of the JSON file in storage
            
        Returns:
            The parsed JSON data
        """
        try:
            content = self.get_file(object_name)
            return json.loads(content)
        except Exception as e:
            raise StorageError(f"Failed to retrieve JSON: {str(e)}")

    def delete_file(self, object_name: str) -> None:
        """
        Delete a file from storage.
        
        Args:
            object_name: Name of the file to delete
        """
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            raise StorageError(f"Failed to delete file: {str(e)}")

class StorageError(Exception):
    """Custom exception for storage operations."""
    pass

# Create a singleton instance
storage = StorageService()
