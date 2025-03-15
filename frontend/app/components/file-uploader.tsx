"use client"

import * as React from "react"
import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload } from "lucide-react"
import { toast } from "sonner"

import { api } from "@/lib/api"
import { Progress } from "@/ui/progress"
import { Loading } from "@/ui/loading"
import { FileBadge } from "@/ui/badge"
import { useFiles } from "@/lib/contexts/file-context"
import { getMimeType, getFileExtension } from "@/lib/utils"

const ACCEPTED_TYPES = {
  'text/csv': ['.csv'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'message/rfc822': ['.eml'],
  'application/epub+zip': ['.epub'],
  'text/html': ['.html'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'text/markdown': ['.md'],
  'application/vnd.ms-outlook': ['.ost', '.pst'],
  'application/pdf': ['.pdf'],
  'image/png': ['.png'],
  'text/x-rst': ['.rst'],
  'application/rtf': ['.rtf'],
  'application/sql': ['.sql'],
  'application/x-tar': ['.tar'],
  'text/tab-separated-values': ['.tsv'],
  'text/plain': ['.txt'],
  'audio/wav': ['.wav'],
  'application/vnd.ms-excel': ['.xls'],
  'application/x-mobipocket-ebook': ['.mobi']
}

const MAX_FILE_SIZE = 100 * 1024 * 1024 // 100MB

export function FileUploader() {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const { refreshFiles, setSelectedFileId } = useFiles()
  const [draggedFiles, setDraggedFiles] = useState<File[]>([])

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    setUploading(true)
    setProgress(0)

    try {
      for (const file of acceptedFiles) {
        setProgress(25) // Start progress
        const response = await api.uploadFile(file)
        
        if (response.error) {
          throw new Error(response.error)
        }

        if (response.data) {
          setProgress(75) // Almost done
          toast.success(`Successfully uploaded ${file.name}`)
          setSelectedFileId(response.data.id)
          setProgress(100)
        }
      }

      // Refresh the file list after uploads
      await refreshFiles()
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Upload failed'
      toast.error(message)
      setProgress(0)
    } finally {
      setUploading(false)
      setDraggedFiles([])
      // Reset progress after a delay to show completion
      setTimeout(() => setProgress(0), 1000)
    }
  }, [refreshFiles, setSelectedFileId])

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject
  } = useDropzone({
    onDrop,
    accept: ACCEPTED_TYPES,
    maxSize: MAX_FILE_SIZE,
    multiple: true,
    onDropRejected: (rejections) => {
      rejections.forEach(({ file, errors }) => {
        const message = errors.map(e => e.message).join(', ')
        toast.error(`${file.name}: ${message}`)
      })
    },
    onDropAccepted: (files) => {
      setDraggedFiles(files)
    }
  })

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-12
        flex flex-col items-center justify-center gap-4
        cursor-pointer transition-colors
        ${isDragAccept ? 'border-green-500 bg-green-50/50' : ''}
        ${isDragReject ? 'border-red-500 bg-red-50/50' : ''}
        ${!isDragActive ? 'border-border hover:border-primary/50' : ''}
        ${uploading ? 'pointer-events-none opacity-50' : ''}
      `}
    >
      <input {...getInputProps()} />
      {uploading ? (
        <Loading text="Uploading files..." />
      ) : (
        <Upload className="h-10 w-10 text-muted-foreground" />
      )}
      <div className="text-center space-y-2">
        <h3 className="text-lg font-medium">
          {isDragActive 
            ? isDragAccept 
              ? 'Drop files to upload'
              : 'Some files are not supported'
            : 'Drag and drop files'}
        </h3>
        <p className="text-sm text-muted-foreground">
          or click to select files (max 100MB each)
        </p>
      </div>

      {draggedFiles.length > 0 && !uploading && (
        <div className="flex flex-wrap gap-2 max-w-md">
          {draggedFiles.map((file, i) => (
            <FileBadge key={i} type={getFileExtension(file.name)} />
          ))}
        </div>
      )}

      {uploading && progress > 0 && (
        <div className="w-full max-w-xs">
          <Progress value={progress} className="h-2" />
          <p className="mt-2 text-sm text-center text-muted-foreground">
            {progress}% complete
          </p>
        </div>
      )}
    </div>
  )
}
