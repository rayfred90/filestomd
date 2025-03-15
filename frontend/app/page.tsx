"use client"

import { FileUploader } from "@/components/file-uploader"
import { ConversionTable } from "@/components/conversion-table"
import { FileLayout, FileContainer } from "@/components/file-layout"
import { PageHeading } from "@/components/ui/heading"
import { FileProvider } from "@/lib/contexts/file-context"

export default function Home() {
  return (
    <FileProvider>
      <main className="container mx-auto py-10 h-[calc(100vh-40px)]">
        <PageHeading
          title="File to Markdown Converter"
          description="Convert various file types to Markdown with embedded metadata"
        />

        <FileLayout>
          <FileContainer>
            <FileUploader />
            <ConversionTable />
          </FileContainer>
        </FileLayout>
      </main>
    </FileProvider>
  )
}

export const metadata = {
  title: 'File to Markdown Converter',
  description: 'Convert various file types to Markdown with embedded metadata',
  metadataBase: new URL('http://localhost:3000'),
  openGraph: {
    title: 'File to Markdown Converter',
    description: 'Convert various file types to Markdown with embedded metadata',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'File to Markdown Converter',
    description: 'Convert various file types to Markdown with embedded metadata',
  },
}
