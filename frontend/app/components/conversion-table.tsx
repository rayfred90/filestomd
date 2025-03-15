"use client"

import * as React from "react"
import { Check, X, FileText } from "lucide-react"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/ui/table"
import { Progress } from "@/ui/progress"
import { Button } from "@/ui/button"
import { Loading } from "@/ui/loading"
import { Error } from "@/ui/error"
import { StatusBadge, FileBadge } from "@/ui/badge"
import type { ConversionFile } from "@/lib/types"
import { formatBytes } from "@/lib/config"
import { useFiles } from "@/lib/contexts/file-context"
import { getFileExtension } from "@/lib/utils"
import { FileActions } from "./file-actions"

export function ConversionTable() {
  const { files, loading, error, selectedFileId, setSelectedFileId } = useFiles()

  const getStatusIcon = (status: ConversionFile['status']) => {
    switch (status) {
      case 'pending':
        return <Loading size="sm" />
      case 'processing':
        return <Loading size="sm" className="text-primary" />
      case 'completed':
        return <Check className="h-4 w-4 text-green-500" />
      case 'failed':
        return <X className="h-4 w-4 text-destructive" />
      default:
        return null
    }
  }

  if (loading) {
    return <Loading center text="Loading files..." />
  }

  if (error) {
    return <Error title="Failed to load files" message={error} />
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>File Name</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Progress</TableHead>
            <TableHead className="text-right">Size</TableHead>
            <TableHead className="w-[100px]">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {files.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={6}
                className="text-center text-muted-foreground h-24"
              >
                <div className="flex flex-col items-center gap-2">
                  <FileText className="h-8 w-8 text-muted-foreground/50" />
                  <p>No files converted yet</p>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            files.map((file) => (
              <TableRow 
                key={file.id}
                className={file.id === selectedFileId ? "bg-muted" : undefined}
              >
                <TableCell>{file.filename}</TableCell>
                <TableCell>
                  <FileBadge type={getFileExtension(file.filename)} />
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {getStatusIcon(file.status)}
                    <StatusBadge status={file.status} />
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Progress
                      value={
                        file.status === 'completed'
                          ? 100
                          : file.status === 'failed'
                          ? 0
                          : file.status === 'processing'
                          ? 50
                          : 0
                      }
                      className="w-[100px]"
                    />
                    {file.error_message && (
                      <Error
                        message={file.error_message}
                        className="ml-2 py-1 px-2 text-xs"
                      />
                    )}
                  </div>
                </TableCell>
                <TableCell className="text-right">
                  {formatBytes(file.file_size)}
                </TableCell>
                <TableCell>
                  <div className="flex justify-end">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => setSelectedFileId(
                        selectedFileId === file.id ? null : file.id
                      )}
                      disabled={file.status !== 'completed'}
                      className="mr-2 hover:bg-background"
                    >
                      <FileText className="h-4 w-4" />
                      <span className="sr-only">View file content</span>
                    </Button>
                    <FileActions file={file} />
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}
