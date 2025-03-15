from typing import Dict, Any, BinaryIO
import csv
import io
from .base_processor import BaseProcessor
from ..utils.chunker import DocumentChunker

class CsvProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.chunker = DocumentChunker(max_chunk_size=500)  # Smaller chunks for tabular data

    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """Process a CSV file and extract its content with metadata."""
        # Read CSV content
        text_content = file.read().decode('utf-8')
        file.seek(0)  # Reset file pointer
        
        # Parse CSV
        csv_reader = csv.reader(io.StringIO(text_content))
        headers = next(csv_reader, [])  # Get headers
        rows = list(csv_reader)
        
        # Extract metadata
        metadata = self._extract_metadata(headers, rows)
        
        # Convert to markdown table
        markdown_content = self._convert_to_markdown(headers, rows)
        
        # Generate chunks (chunk by groups of rows)
        chunks = self._create_chunks(headers, rows, metadata)
        
        return {
            'content': text_content,
            'markdown': markdown_content,
            'metadata': metadata,
            'chunks': chunks
        }

    def _extract_metadata(self, headers: list, rows: list) -> Dict[str, Any]:
        """Extract metadata from the CSV content."""
        column_types = self._infer_column_types(headers, rows)
        
        return {
            'column_count': len(headers),
            'row_count': len(rows),
            'headers': headers,
            'column_types': column_types,
            'has_headers': bool(headers),
            'total_cells': len(headers) * len(rows) if headers else 0
        }

    def _infer_column_types(self, headers: list, rows: list) -> Dict[str, str]:
        """Infer data types for each column."""
        if not rows:
            return {header: 'unknown' for header in headers}

        types = {}
        for idx, header in enumerate(headers):
            column_values = [row[idx] for row in rows if len(row) > idx]
            types[header] = self._detect_type(column_values)
        
        return types

    def _detect_type(self, values: list) -> str:
        """Detect the data type of a column based on its values."""
        numeric_count = 0
        date_count = 0
        empty_count = 0
        total_count = len(values)
        
        if not total_count:
            return 'unknown'

        for value in values:
            if not value.strip():
                empty_count += 1
                continue

            # Try numeric
            try:
                float(value)
                numeric_count += 1
                continue
            except ValueError:
                pass
            
            # Try date (basic check)
            if any(c in value for c in ['/', '-']) and sum(c.isdigit() for c in value) > 5:
                date_count += 1

        # Account for empty values in determination
        non_empty_count = total_count - empty_count
        if non_empty_count == 0:
            return 'empty'
            
        # Determine type based on majority
        if numeric_count / non_empty_count > 0.8:
            return 'numeric'
        elif date_count / non_empty_count > 0.8:
            return 'date'
        return 'text'

    def _convert_to_markdown(self, headers: list, rows: list) -> str:
        """Convert CSV content to Markdown table format."""
        if not headers and not rows:
            return ""

        markdown_lines = []
        
        # Add headers
        markdown_lines.append('| ' + ' | '.join(headers) + ' |')
        
        # Add separator with alignment
        separators = []
        for _ in headers:
            separators.append('---')  # Default center alignment
        markdown_lines.append('| ' + ' | '.join(separators) + ' |')
        
        # Add rows
        for row in rows:
            # Ensure row has same number of columns as headers
            padded_row = row + [''] * (len(headers) - len(row))
            # Escape pipe characters and format cells
            escaped_row = [
                str(cell).replace('|', '\\|')
                    .replace('\n', '<br>')  # Handle newlines
                    .replace('\r', '')
                for cell in padded_row[:len(headers)]
            ]
            markdown_lines.append('| ' + ' | '.join(escaped_row) + ' |')

        return '\n'.join(markdown_lines)

    def _create_chunks(self, headers: list, rows: list, metadata: Dict[str, Any]) -> list:
        """Create chunks from CSV data, grouping rows together."""
        ROWS_PER_CHUNK = 25  # Smaller chunks for better readability
        chunks = []
        
        for i in range(0, len(rows), ROWS_PER_CHUNK):
            chunk_rows = rows[i:i + ROWS_PER_CHUNK]
            
            # Convert chunk to markdown table
            chunk_content = self._convert_to_markdown(headers, chunk_rows)
            
            # Create chunk metadata
            chunk_metadata = {
                **metadata,  # Include all base metadata
                'row_range': {
                    'start': i + 1,  # 1-based indexing for display
                    'end': min(i + ROWS_PER_CHUNK, len(rows))
                },
                'row_count': len(chunk_rows),
                'is_first_chunk': i == 0,
                'is_last_chunk': i + ROWS_PER_CHUNK >= len(rows)
            }
            
            chunks.append({
                'content': chunk_content,
                'metadata': chunk_metadata
            })
        
        return chunks
