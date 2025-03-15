"use client"

import * as React from "react"
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from "@/components/ui/resizable"
import { FilePreview } from "./file-preview"
import { useFiles } from "@/lib/contexts/file-context"
import { Heading } from "@/components/ui/heading"

interface FileLayoutProps {
  children: React.ReactNode;
}

export function FileLayout({ children }: FileLayoutProps) {
  const { selectedFileId, files } = useFiles()
  const selectedFile = files.find(f => f.id === selectedFileId)

  return (
    <ResizablePanelGroup 
      direction="horizontal" 
      className="min-h-[calc(100vh-220px)]"
    >
      <ResizablePanel defaultSize={60} minSize={40}>
        <div className="h-full">
          {children}
        </div>
      </ResizablePanel>

      <ResizableHandle withHandle />

      <ResizablePanel defaultSize={40} minSize={30}>
        <div className="h-full p-6 overflow-auto">
          {selectedFileId ? (
            <div className="space-y-6">
              <Heading
                title={selectedFile?.filename || 'File Preview'}
                description={`View the converted content and metadata for ${selectedFile?.filename}`}
              />
              <FilePreview fileId={selectedFileId} />
            </div>
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              <p>Select a file to view its content</p>
            </div>
          )}
        </div>
      </ResizablePanel>
    </ResizablePanelGroup>
  )
}

export function FileContainer({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-8">
      <Heading
        title="Files"
        description="Upload files and view their conversion status"
      />
      {children}
    </div>
  )
}
