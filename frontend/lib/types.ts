export type FileStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface FileMetadata {
  title?: string;
  author?: string;
  subject?: string;
  creator?: string;
  producer?: string;
  creation_date?: string;
  modification_date?: string;
  page_count?: number;
  word_count?: number;
  chunk_count?: number;
  positions?: Array<{
    page: number;
    x: number;
    y: number;
    width?: number;
    height?: number;
    content: string;
    confidence?: number;
  }>;
}

export interface ConversionFile {
  id: string;
  filename: string;
  original_type: string;
  file_size: number;
  status: FileStatus;
  error_message?: string;
  metadata?: FileMetadata;
  markdown_path?: string;
  json_path?: string;
  created_at: string;
  updated_at: string;
  page_count?: number;
  word_count?: number;
  chunk_count?: number;
}

export interface ChunkMetadata {
  id: string;
  file_id: string;
  content: string;
  metadata: Record<string, any>;
  sequence_number: number;
  created_at: string;
}
