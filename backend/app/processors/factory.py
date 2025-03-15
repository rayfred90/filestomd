from typing import Type
from pathlib import Path
from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .docx_processor import DocxProcessor
from .csv_processor import CsvProcessor
from .txt_processor import TextProcessor
from .code_processor import CodeProcessor
from .xlsx_processor import XlsxProcessor
from ..models.file_model import File

class ProcessorFactory:
    """Factory for creating file processors based on file type."""
    
    _processors = {
        # Document types
        "pdf": PDFProcessor,
        "csv": CsvProcessor,
        "docx": DocxProcessor,
        "txt": TextProcessor,
        
        # Spreadsheet types
        "xlsx": XlsxProcessor,
        "xls": XlsxProcessor,  # Note: older Excel format support
        
        # Code file types
        "py": CodeProcessor,
        "js": CodeProcessor,
        "jsx": CodeProcessor,
        "ts": CodeProcessor,
        "tsx": CodeProcessor,
        "java": CodeProcessor,
        "cpp": CodeProcessor,
        "c": CodeProcessor,
        "cs": CodeProcessor,
        "go": CodeProcessor,
        "rb": CodeProcessor,
        "php": CodeProcessor,
        "rs": CodeProcessor,
        "swift": CodeProcessor,
        "kt": CodeProcessor,
        
        # Web technologies
        "html": CodeProcessor,
        "css": CodeProcessor,
        "scss": CodeProcessor,
        "less": CodeProcessor,
        "json": CodeProcessor,
        "xml": CodeProcessor,
        "yaml": CodeProcessor,
        "yml": CodeProcessor,
        
        # Shell scripts
        "sh": CodeProcessor,
        "bash": CodeProcessor,
        "zsh": CodeProcessor,
        "fish": CodeProcessor,
        "ps1": CodeProcessor,
        "bat": CodeProcessor,
        "cmd": CodeProcessor,
        
        # Configuration files
        "ini": CodeProcessor,
        "conf": CodeProcessor,
        "cfg": CodeProcessor,
        "toml": CodeProcessor,
        
        # Database
        "sql": CodeProcessor,
    }

    @classmethod
    def get_processor_class(cls, file_extension: str) -> Type[BaseProcessor]:
        """Get the appropriate processor class for a file type."""
        
        # Convert extension to lowercase without leading dot
        ext = file_extension.lower().lstrip(".")
        
        # Check if we have a processor for this file type
        processor_class = cls._processors.get(ext)
        if not processor_class:
            # Default to text processor for unknown types
            return TextProcessor
        
        return processor_class

    @classmethod
    def create_processor(cls, file_path: str | Path, file_info: File) -> BaseProcessor:
        """Create a processor instance for a file."""
        
        # Convert to Path object if string
        path = Path(file_path)
        
        # Get file extension
        if not path.suffix:
            raise ValueError(f"File has no extension: {file_path}")
        
        # Get processor class
        processor_class = cls.get_processor_class(path.suffix[1:])
        
        # Create and return processor instance
        return processor_class(str(path), file_info)

    @classmethod
    def register_processor(
        cls, 
        extension: str, 
        processor_class: Type[BaseProcessor]
    ) -> None:
        """Register a new processor for a file type."""
        if not issubclass(processor_class, BaseProcessor):
            raise ValueError(
                f"Processor class must inherit from BaseProcessor: {processor_class}"
            )
        
        ext = extension.lower().lstrip(".")
        cls._processors[ext] = processor_class

class UnsupportedFileType(Exception):
    """Raised when trying to process an unsupported file type."""
    pass
