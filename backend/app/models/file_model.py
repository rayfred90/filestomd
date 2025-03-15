from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class FileStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileBase(SQLModel):
    filename: str
    original_type: str
    file_size: int
    status: FileStatus = Field(default=FileStatus.PENDING)
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Field(JSON))
    markdown_path: Optional[str] = None
    json_path: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    chunk_count: Optional[int] = None

class File(FileBase, table=True):
    __tablename__ = "files"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ChunkBase(SQLModel):
    file_id: UUID = Field(foreign_key="files.id")
    content: str
    metadata: Dict[str, Any] = Field(sa_column=Field(JSON))
    sequence_number: int

class Chunk(ChunkBase, table=True):
    __tablename__ = "chunks"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PositionBase(SQLModel):
    file_id: UUID = Field(foreign_key="files.id")
    page_number: int
    x_coord: float
    y_coord: float
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Field(JSON))

class Position(PositionBase, table=True):
    __tablename__ = "positions"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class FileResponse(FileBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class ChunkResponse(ChunkBase):
    id: UUID
    created_at: datetime

class PositionResponse(PositionBase):
    id: UUID
    created_at: datetime
