"use client"

import * as React from "react"
import { MoreHorizontal, Download, Trash2, Eye } from "lucide-react"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/ui/dropdown-menu"
import { Button } from "@/ui/button"
import { toast } from "sonner"
import { api } from "@/lib/api"
import { useFiles } from "@/lib/contexts/file-context"
import type { ConversionFile } from "@/lib/types"

interface FileActionsProps {
  file: ConversionFile;
}

export function FileActions({ file }: FileActionsProps) {
  const { refreshFiles, setSelectedFileId } = useFiles()

  const handlePreview = () => {
    setSelectedFileId(file.id)
  }

  const handleDownload = async () => {
    // Implement download logic using the API
    toast.info('Download starting...')
  }

  const handleDelete = async () => {
    try {
      const response = await api.deleteFile(file.id)
      if (response.error) {
        throw new Error(response.error)
      }
      toast.success('File deleted successfully')
      setSelectedFileId(null)
      refreshFiles()
    } catch (error) {
      toast.error('Failed to delete file')
    }
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="hover:bg-background"
        >
          <MoreHorizontal className="h-4 w-4" />
          <span className="sr-only">Open menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem 
          onClick={handlePreview}
          disabled={file.status !== 'completed'}
        >
          <Eye className="mr-2 h-4 w-4" />
          Preview
        </DropdownMenuItem>
        <DropdownMenuItem 
          onClick={handleDownload}
          disabled={file.status !== 'completed'}
        >
          <Download className="mr-2 h-4 w-4" />
          Download
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem 
          onClick={handleDelete}
          className="text-red-600 focus:text-red-600 focus:bg-red-50"
        >
          <Trash2 className="mr-2 h-4 w-4" />
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
