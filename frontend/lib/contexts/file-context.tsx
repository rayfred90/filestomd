"use client"

import * as React from "react"
import { api } from "@/lib/api"
import type { ConversionFile } from "@/lib/types"

interface FileContextType {
  files: ConversionFile[];
  loading: boolean;
  error: string | null;
  selectedFileId: string | null;
  setSelectedFileId: (id: string | null) => void;
  refreshFiles: () => Promise<void>;
}

export const FileContext = React.createContext<FileContextType>({
  files: [],
  loading: false,
  error: null,
  selectedFileId: null,
  setSelectedFileId: () => {},
  refreshFiles: async () => {},
})

export function useFiles() {
  return React.useContext(FileContext)
}

export function FileProvider({ children }: { children: React.ReactNode }) {
  const [files, setFiles] = React.useState<ConversionFile[]>([])
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)
  const [selectedFileId, setSelectedFileId] = React.useState<string | null>(null)

  const refreshFiles = React.useCallback(async () => {
    setLoading(true)
    const response = await api.listFiles()
    if (response.error) {
      setError(response.error)
    } else if (response.data) {
      setFiles(response.data)
      setError(null)
    }
    setLoading(false)
  }, [])

  React.useEffect(() => {
    refreshFiles()
    // Set up polling for updates
    const interval = setInterval(refreshFiles, 5000)
    return () => clearInterval(interval)
  }, [refreshFiles])

  const value = React.useMemo(() => ({
    files,
    loading,
    error,
    selectedFileId,
    setSelectedFileId,
    refreshFiles,
  }), [files, loading, error, selectedFileId, refreshFiles])

  return (
    <FileContext.Provider value={value}>
      {children}
    </FileContext.Provider>
  )
}
