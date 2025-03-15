import pdfplumber
import PyPDF2
from typing import Dict, Any, List
from .base_processor import BaseProcessor
from ..models.file_model import File

class PDFProcessor(BaseProcessor):
    """Processor for PDF files."""
    
    async def extract_text(self) -> str:
        text = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n\n".join(text)

    async def extract_metadata(self) -> Dict[str, Any]:
        metadata = {}
        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            info = reader.metadata
            if info:
                metadata.update({
                    "title": info.get("/Title", ""),
                    "author": info.get("/Author", ""),
                    "subject": info.get("/Subject", ""),
                    "creator": info.get("/Creator", ""),
                    "producer": info.get("/Producer", ""),
                    "creation_date": info.get("/CreationDate", ""),
                    "modification_date": info.get("/ModDate", ""),
                })
            
            metadata.update({
                "page_count": len(reader.pages),
                "file_type": "pdf",
                "encrypted": reader.is_encrypted,
            })
            
        return metadata

    async def get_positions(self) -> List[Dict[str, Any]]:
        positions = []
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                words = page.extract_words()
                for word in words:
                    positions.append({
                        "page": page_num,
                        "x": word["x0"],
                        "y": word["top"],
                        "width": word["x1"] - word["x0"],
                        "height": word["bottom"] - word["top"],
                        "content": word["text"],
                        "confidence": 1.0,  # PDF text extraction typically has high confidence
                    })
        
        return positions

    async def process(self) -> tuple[str, str, Dict[str, Any]]:
        """Process PDF file and extract all information."""
        try:
            # Get base processing
            markdown, json_content, metadata = await super().process()
            
            # Add PDF-specific metadata
            with pdfplumber.open(self.file_path) as pdf:
                metadata.update({
                    "page_sizes": [
                        {"width": page.width, "height": page.height}
                        for page in pdf.pages
                    ],
                })
            
            return markdown, json_content, metadata
            
        except Exception as e:
            raise ProcessingError(f"Error processing PDF: {str(e)}")
