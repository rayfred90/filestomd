"use client"

import * as React from "react"
import { useState } from "react"
import { FileText, Code } from "lucide-react"

import { api } from "@/lib/api"
import { Button } from "@/ui/button"
import { Loading } from "@/ui/loading"
import { Error } from "@/ui/error"
import { toast } from "sonner"
import { useMemo } from "react"
import { StatusBadge, FileBadge } from "@/ui/badge"
import { useFiles } from "@/lib/contexts/file-context"
import { getFileExtension } from "@/lib/utils"

interface ContentData {
  content: string;
  metadata: Record<string, any>;
}

interface ContentState {
  markdown?: string;
  json?: string;
  metadata?: Record<string, any>;
  loading: boolean;
  error: string | null;
  view: 'markdown' | 'json';
}

export function FilePreview({ fileId }: { fileId: string }) {
  const { files } = useFiles()
  const file = files.find(f => f.id === fileId)
  const [state, setState] = useState<ContentState>({
    loading: true,
    error: null,
    view: 'markdown'
  })

  const fetchContent = React.useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))

    const response = await api.getFileContent(fileId, state.view)
    
    if (response.error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: response.error || 'An unknown error occurred'
      }))
      toast.error(`Failed to load content: ${response.error}`)
    } else if (response.data && 'content' in response.data) {
      const data = response.data as ContentData
      setState(prev => ({
        ...prev,
        loading: false,
        error: null,
        [state.view]: data.content,
        metadata: data.metadata
      }))
    } else {
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Invalid response format'
      }))
      toast.error('Invalid response format from server')
    }
  }, [fileId, state.view])

  React.useEffect(() => {
    fetchContent()
  }, [fetchContent])

  const formattedContent = useMemo(() => {
    if (state[state.view] && state.view === 'json') {
      try {
        return JSON.stringify(JSON.parse(state.json!), null, 2)
      } catch {
        return state.json
      }
    }
    return state[state.view]
  }, [state])

  const setView = (view: 'markdown' | 'json') => {
    setState(prev => ({ ...prev, view }))
  }

  if (state.loading) {
    return <Loading center text="Loading content..." />
  }

  if (state.error) {
    return <Error title="Failed to load content" message={state.error} />
  }

  return (
    <div className="space-y-6">
      {file && (
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <FileBadge type={getFileExtension(file.filename)} />
            <StatusBadge status={file.status} />
          </div>
        </div>
      )}

      <div className="flex items-center gap-4">
        <Button
          variant={state.view === 'markdown' ? 'default' : 'outline'}
          onClick={() => setView('markdown')}
        >
          <FileText className="h-4 w-4 mr-2" />
          Markdown
        </Button>
        <Button
          variant={state.view === 'json' ? 'default' : 'outline'}
          onClick={() => setView('json')}
        >
          <Code className="h-4 w-4 mr-2" />
          JSON
        </Button>
      </div>

      <div className="rounded-md border bg-muted/50 p-4">
        <pre className="overflow-auto max-h-[60vh] text-sm">
          <code>
            {formattedContent || `No ${state.view} content available`}
          </code>
        </pre>
      </div>

      {state.metadata && (
        <div className="rounded-md border p-4 space-y-2">
          <h3 className="font-medium">Metadata</h3>
          <pre className="text-sm overflow-auto bg-muted/50 p-2 rounded">
            <code>
              {JSON.stringify(state.metadata, null, 2)}
            </code>
          </pre>
        </div>
      )}
    </div>
  )
}
