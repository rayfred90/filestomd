from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List
from pathlib import Path
from ..models.file_model import File

class BaseProcessor(ABC):
    """
    Abstract base class for file processors.
    All specific file type processors must inherit from this class.
    """
    
    def __init__(self, file_path: str, file_info: File):
        self.file_path = Path(file_path)
        self.file_info = file_info
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @abstractmethod
    async def extract_text(self) -> str:
        """Extract raw text content from the file."""
        pass

    @abstractmethod
    async def extract_metadata(self) -> Dict[str, Any]:
        """Extract metadata from the file."""
        pass

    @abstractmethod
    async def get_positions(self) -> List[Dict[str, Any]]:
        """Get positions of text elements in the document."""
        pass

    async def process(self) -> Tuple[str, str, Dict[str, Any]]:
        """
        Process the file and return markdown, JSON, and metadata.
        
        Returns:
            Tuple containing:
            - Markdown content (str)
            - JSON content (str)
            - Metadata (Dict[str, Any])
        """
        try:
            # Extract text and metadata
            text = await self.extract_text()
            metadata = await self.extract_metadata()
            positions = await self.get_positions()
            
            # Add positions to metadata
            metadata["positions"] = positions
            
            # Generate markdown
            markdown = self.text_to_markdown(text, metadata)
            
            # Generate JSON
            json_content = {
                "content": text,
                "metadata": metadata
            }
            
            return markdown, json_content, metadata
            
        except Exception as e:
            raise ProcessingError(f"Error processing file: {str(e)}")

    def text_to_markdown(self, text: str, metadata: Dict[str, Any]) -> str:
        """Convert text content to markdown format with metadata."""
        # Add metadata as YAML front matter
        markdown = "---\n"
        for key, value in metadata.items():
            if key != "positions":  # Skip positions in front matter
                markdown += f"{key}: {value}\n"
        markdown += "---\n\n"
        
        # Add content
        markdown += text
        
        return markdown

class ProcessingError(Exception):
    """Custom exception for processing errors."""
    pass
