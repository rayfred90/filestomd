from typing import Dict, Any, BinaryIO
import re
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import MarkdownFormatter
from .base_processor import BaseProcessor
from ..utils.chunker import DocumentChunker

class CodeProcessor(BaseProcessor):
    """Processor for source code files with syntax highlighting."""

    # Map of file extensions to language names
    LANGUAGE_MAP = {
        # Common programming languages
        'py': 'python',
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'cs': 'csharp',
        'go': 'go',
        'rb': 'ruby',
        'php': 'php',
        'rs': 'rust',
        'swift': 'swift',
        'kt': 'kotlin',
        
        # Web technologies
        'html': 'html',
        'css': 'css',
        'scss': 'scss',
        'less': 'less',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        
        # Shell scripts
        'sh': 'bash',
        'bash': 'bash',
        'zsh': 'bash',
        'fish': 'fish',
        'ps1': 'powershell',
        'bat': 'batch',
        'cmd': 'batch',
        
        # Configuration files
        'ini': 'ini',
        'conf': 'ini',
        'cfg': 'ini',
        'toml': 'toml',
        
        # Database
        'sql': 'sql',
    }

    def __init__(self):
        super().__init__()
        self.chunker = DocumentChunker(max_chunk_size=2000)  # Larger chunks for code

    def process(self, file: BinaryIO) -> Dict[str, Any]:
        """Process a code file and extract its content with metadata."""
        # Read code content
        try:
            code_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 fails
            file.seek(0)
            code_content = file.read().decode('latin-1')
        
        # Clean and normalize line endings
        code_content = self._normalize_line_endings(code_content)
        
        # Extract metadata
        metadata = self._extract_metadata(code_content)
        
        # Generate chunks (by logical blocks)
        chunks = self._chunk_code(code_content, metadata)
        
        # Convert to markdown with syntax highlighting
        markdown_content = self._convert_to_markdown(code_content, metadata['language'])
        
        return {
            'content': code_content,
            'markdown': markdown_content,
            'metadata': metadata,
            'chunks': chunks
        }

    def _normalize_line_endings(self, text: str) -> str:
        """Normalize line endings to Unix style."""
        return text.replace('\r\n', '\n').replace('\r', '\n')

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from code content."""
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Detect language from file extension
        file_ext = self._get_file_extension()
        language = self.LANGUAGE_MAP.get(file_ext.lower(), 'text')
        
        # Calculate code metrics
        return {
            'language': language,
            'loc': len(non_empty_lines),  # Lines of code
            'total_lines': len(lines),
            'blank_lines': len(lines) - len(non_empty_lines),
            'char_count': len(content),
            'average_line_length': sum(len(line) for line in non_empty_lines) / (len(non_empty_lines) or 1),
            'has_shebang': content.startswith('#!'),
            'encoding': 'utf-8',
            'functions': self._count_functions(content, language),
            'classes': self._count_classes(content, language),
            'comments': self._count_comments(content, language)
        }

    def _count_functions(self, content: str, language: str) -> int:
        """Count function definitions in code."""
        patterns = {
            'python': r'def\s+\w+\s*\(',
            'javascript': r'(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|async\s+function\s*\w+)\s*\(',
            'typescript': r'(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(|async\s+function\s*\w+)\s*\(',
            'java': r'(?:public|private|protected|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *\{?',
            'cpp': r'[\w\<\>\[\]]+\s+(\w+)\s*\([^\)]*\)\s*\{?',
            'go': r'func\s+\w+\s*\(',
        }
        pattern = patterns.get(language, r'function\s+\w+|def\s+\w+')
        return len(re.findall(pattern, content))

    def _count_classes(self, content: str, language: str) -> int:
        """Count class definitions in code."""
        patterns = {
            'python': r'class\s+\w+(?:\(.*\))?:',
            'javascript': r'class\s+\w+',
            'typescript': r'class\s+\w+',
            'java': r'class\s+\w+',
            'cpp': r'class\s+\w+',
            'go': r'type\s+\w+\s+struct',
        }
        pattern = patterns.get(language, r'class\s+\w+')
        return len(re.findall(pattern, content))

    def _count_comments(self, content: str, language: str) -> Dict[str, int]:
        """Count different types of comments in code."""
        single_line_patterns = {
            'python': r'#.*$',
            'javascript': r'//.*$',
            'typescript': r'//.*$',
            'java': r'//.*$',
            'cpp': r'//.*$',
            'go': r'//.*$',
        }
        multi_line_patterns = {
            'python': r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'',
            'javascript': r'/\*[\s\S]*?\*/',
            'typescript': r'/\*[\s\S]*?\*/',
            'java': r'/\*[\s\S]*?\*/',
            'cpp': r'/\*[\s\S]*?\*/',
            'go': r'/\*[\s\S]*?\*/',
        }
        
        single_pattern = single_line_patterns.get(language, r'(?:#|//).*$')
        multi_pattern = multi_line_patterns.get(language, r'/\*[\s\S]*?\*/|"""[\s\S]*?"""')
        
        return {
            'single_line': len(re.findall(single_pattern, content, re.MULTILINE)),
            'multi_line': len(re.findall(multi_pattern, content))
        }

    def _chunk_code(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk code into logical blocks (e.g., functions, classes, or sections).
        Falls back to chunker for languages without specific chunking rules.
        """
        language = metadata['language']
        
        # For supported languages, try to chunk by logical blocks
        if language in ['python', 'javascript', 'typescript', 'java']:
            chunks = self._chunk_by_definitions(content, language)
            if chunks:
                return chunks
        
        # Fallback to regular chunking
        return self.chunker.chunk_text(content, metadata)

    def _chunk_by_definitions(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Attempt to chunk code by function/class definitions."""
        chunks = []
        
        # Pattern to match function/class definitions
        if language == 'python':
            pattern = r'^(?:def|class)\s+\w+[^\n]*(?:\n(?:[ \t].*|$))*'
        elif language in ['javascript', 'typescript']:
            pattern = r'^(?:function|class|const\s+\w+\s*=\s*(?:async\s*)?\()[^\n]*(?:\n(?:[ \t].*|$))*'
        elif language == 'java':
            pattern = r'^(?:public|private|protected|class)\s+[^\n]*(?:\n(?:[ \t].*|$))*'
        else:
            return []
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        last_end = 0
        
        for match in matches:
            # Add any content before this match as a chunk
            if match.start() > last_end:
                preceding = content[last_end:match.start()].strip()
                if preceding:
                    chunks.append({
                        'content': preceding,
                        'metadata': {
                            'type': 'code_block',
                            'start_line': content.count('\n', 0, last_end) + 1,
                            'end_line': content.count('\n', 0, match.start()) + 1
                        }
                    })
            
            # Add the matched definition as a chunk
            definition = match.group(0)
            chunks.append({
                'content': definition.strip(),
                'metadata': {
                    'type': 'definition',
                    'name': re.match(r'^(?:def|class|function|const)?\s*(\w+)', definition).group(1),
                    'start_line': content.count('\n', 0, match.start()) + 1,
                    'end_line': content.count('\n', 0, match.end()) + 1
                }
            })
            
            last_end = match.end()
        
        # Add any remaining content
        if last_end < len(content):
            remaining = content[last_end:].strip()
            if remaining:
                chunks.append({
                    'content': remaining,
                    'metadata': {
                        'type': 'code_block',
                        'start_line': content.count('\n', 0, last_end) + 1,
                        'end_line': content.count('\n') + 1
                    }
                })
        
        return chunks

    def _convert_to_markdown(self, content: str, language: str) -> str:
        """Convert code to markdown with syntax highlighting."""
        try:
            lexer = get_lexer_for_filename(f'file.{language}')
        except:
            lexer = TextLexer()
        
        formatter = MarkdownFormatter(style='monokai')
        highlighted = highlight(content, lexer, formatter)
        
        # Ensure proper markdown code block formatting
        return f'```{language}\n{content}\n```'

    def _get_file_extension(self) -> str:
        """Get the file extension from the current file."""
        # This would typically come from the file path
        # For now, return a default
        return 'txt'  # This should be overridden in actual implementation
