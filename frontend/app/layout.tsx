import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { Toaster } from "sonner"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})

export const metadata: Metadata = {
  title: "Files to Markdown Converter",
  description: "Convert various file types to markdown with embedded metadata",
  icons: {
    icon: "/favicon.ico",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-background font-sans antialiased selection:bg-primary/10">
        {children}
        <Toaster 
          position="bottom-right" 
          richColors 
          closeButton
          theme="system"
        />
      </body>
    </html>
  )
}
