from typing import Dict, Any, BinaryIO
from .base_processor import BaseProcessor
from ..utils.chunker import DocumentChunker

class TextProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.chunker = DocumentChunker()

    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """Process a text file and extract its content with metadata."""
        # Read text content
        try:
            text_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 fails
            file.seek(0)
            text_content = file.read().decode('latin-1')
        
        # Clean and normalize line endings
        text_content = self._normalize_line_endings(text_content)
        
        # Generate metadata
        metadata = self._extract_metadata(text_content)
        
        # Generate chunks
        chunks = self.chunker.chunk_text(text_content, metadata)
        
        # Convert to markdown (for text files, this is minimal processing)
        markdown_content = self._convert_to_markdown(text_content)
        
        return {
            'content': text_content,
            'markdown': markdown_content,
            'metadata': metadata,
            'chunks': chunks
        }

    def _normalize_line_endings(self, text: str) -> str:
        """Normalize line endings to Unix style."""
        return text.replace('\r\n', '\n').replace('\r', '\n')

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from text content."""
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Calculate various text metrics
        return {
            'char_count': len(content),
            'word_count': len(content.split()),
            'line_count': len(lines),
            'non_empty_line_count': len(non_empty_lines),
            'average_line_length': sum(len(line) for line in non_empty_lines) / (len(non_empty_lines) or 1),
            'has_bom': content.startswith('\ufeff'),
            'encoding': 'utf-8'  # We've handled the decoding explicitly
        }

    def _convert_to_markdown(self, content: str) -> str:
        """Convert text content to Markdown format."""
        # For plain text, we primarily need to:
        # 1. Ensure paragraphs are separated by blank lines
        # 2. Escape any markdown special characters
        
        # Split into paragraphs (one or more blank lines)
        paragraphs = content.split('\n\n')
        
        # Process each paragraph
        processed_paragraphs = []
        for para in paragraphs:
            if not para.strip():
                continue
            
            # Escape markdown special characters
            escaped_para = (
                para.replace('\\', '\\\\')
                    .replace('*', '\\*')
                    .replace('_', '\\_')
                    .replace('`', '\\`')
                    .replace('#', '\\#')
                    .replace('>', '\\>')
                    .replace('-', '\\-')
                    .replace('+', '\\+')
                    .replace('[', '\\[')
                    .replace(']', '\\]')
                    .replace('(', '\\(')
                    .replace(')', '\\)')
            )
            
            # Join lines within paragraph
            processed_para = ' '.join(escaped_para.split('\n'))
            processed_paragraphs.append(processed_para)
        
        # Join paragraphs with double newlines
        return '\n\n'.join(processed_paragraphs)
