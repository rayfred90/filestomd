import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatFileSize(bytes: number, decimals = 2) {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

export function getFileExtension(filename: string): string {
  return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2).toLowerCase()
}

export function getMimeType(filename: string): string {
  const ext = getFileExtension(filename)
  const mimeTypes: Record<string, string> = {
    txt: 'text/plain',
    pdf: 'application/pdf',
    doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    md: 'text/markdown',
    html: 'text/html',
    htm: 'text/html',
    rtf: 'application/rtf',
    csv: 'text/csv',
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    gif: 'image/gif',
    epub: 'application/epub+zip',
    mobi: 'application/x-mobipocket-ebook'
  }

  return mimeTypes[ext] || 'application/octet-stream'
}

export function getFileCategory(filename: string): string {
  const ext = getFileExtension(filename)
  const categories: Record<string, string> = {
    // Documents
    pdf: 'document',
    doc: 'document',
    docx: 'document',
    txt: 'document',
    rtf: 'document',
    md: 'document',
    // Web
    html: 'web',
    htm: 'web',
    // Data
    csv: 'data',
    json: 'data',
    xml: 'data',
    // Images
    jpg: 'image',
    jpeg: 'image',
    png: 'image',
    gif: 'image',
    // Ebooks
    epub: 'ebook',
    mobi: 'ebook',
    azw3: 'ebook',
    // Email
    eml: 'email',
    msg: 'email',
    // Archive
    zip: 'archive',
    tar: 'archive',
    gz: 'archive',
  }

  return categories[ext] || 'other'
}

export function isTextFile(filename: string): boolean {
  const textExtensions = [
    'txt', 'md', 'markdown', 'rst', 'html', 'htm', 'css', 'csv', 'json', 'xml'
  ]
  return textExtensions.includes(getFileExtension(filename))
}
