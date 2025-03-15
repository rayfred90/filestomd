from typing import List, Dict, Any, Optional
import re

class DocumentChunker:
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks while preserving semantic boundaries."""
        # Clean and normalize text
        text = self._normalize_text(text)
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            # If adding this sentence would exceed max size, create new chunk
            if current_size + sentence_size > self.max_chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunk_metadata = self._create_chunk_metadata(chunk_text, metadata)
                chunks.append({
                    'content': chunk_text,
                    'metadata': chunk_metadata
                })
                
                # Start new chunk with overlap
                overlap_size = 0
                overlap_chunk = []
                
                # Add sentences from end of previous chunk for overlap
                for prev_sentence in reversed(current_chunk):
                    if overlap_size + len(prev_sentence) > self.overlap:
                        break
                    overlap_chunk.insert(0, prev_sentence)
                    overlap_size += len(prev_sentence)
                
                current_chunk = overlap_chunk
                current_size = overlap_size
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        # Add final chunk if there's remaining content
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_metadata = self._create_chunk_metadata(chunk_text, metadata)
            chunks.append({
                'content': chunk_text,
                'metadata': chunk_metadata
            })
        
        return chunks

    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing extra whitespace and normalizing line endings."""
        # Replace multiple newlines with single newline
        text = re.sub(r'\n\s*\n', '\n', text)
        # Replace other whitespace characters
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex while preserving semantic boundaries."""
        # Basic sentence splitting regex
        # Handles common sentence endings (., !, ?) while avoiding common abbreviations
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [s.strip() for s in sentences if s.strip()]

    def _create_chunk_metadata(self, chunk_text: str, original_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create metadata for a chunk, incorporating original metadata if provided."""
        metadata = {
            'char_count': len(chunk_text),
            'word_count': len(chunk_text.split()),
        }
        
        if original_metadata:
            # Preserve relevant metadata from original document
            for key in ['page', 'section', 'source']:
                if key in original_metadata:
                    metadata[key] = original_metadata[key]
        
        return metadata
