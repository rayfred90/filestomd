import { getApiUrl } from "./config"
import type { ConversionFile } from "./types"

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  private async handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || response.statusText)
    }
    return { data: await response.json() }
  }

  async uploadFile(file: File): Promise<ApiResponse<ConversionFile>> {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(getApiUrl('/files/upload'), {
        method: 'POST',
        body: formData,
      })

      return this.handleResponse<ConversionFile>(response)
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Failed to upload file'
      }
    }
  }

  async listFiles(): Promise<ApiResponse<ConversionFile[]>> {
    try {
      const response = await fetch(getApiUrl('/files/list'))
      return this.handleResponse<ConversionFile[]>(response)
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Failed to fetch files'
      }
    }
  }

  async getFile(fileId: string): Promise<ApiResponse<ConversionFile>> {
    try {
      const response = await fetch(getApiUrl(`/files/${fileId}`))
      return this.handleResponse<ConversionFile>(response)
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Failed to fetch file'
      }
    }
  }

  async getFileContent(fileId: string, type: 'markdown' | 'json' = 'markdown'): Promise<ApiResponse<{
    content: string;
    metadata: Record<string, any>;
  }>> {
    try {
      const response = await fetch(getApiUrl(`/files/${fileId}/content?type=${type}`))
      return this.handleResponse<{
        content: string;
        metadata: Record<string, any>;
      }>(response)
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Failed to fetch file content'
      }
    }
  }

  async deleteFile(fileId: string): Promise<ApiResponse<{ message: string }>> {
    try {
      const response = await fetch(getApiUrl(`/files/${fileId}`), {
        method: 'DELETE'
      })
      return this.handleResponse<{ message: string }>(response)
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Failed to delete file'
      }
    }
  }
}

export const api = new ApiService()
