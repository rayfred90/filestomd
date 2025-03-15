"use client"

import { AlertTriangle, XCircle } from "lucide-react"
import { cn } from "@/lib/utils"

interface ErrorProps {
  title?: string;
  message: string;
  variant?: "warning" | "error";
  className?: string;
}

export function Error({ 
  title, 
  message, 
  variant = "error",
  className 
}: ErrorProps) {
  const Icon = variant === "warning" ? AlertTriangle : XCircle

  return (
    <div className={cn(
      "rounded-md border p-4",
      variant === "warning" 
        ? "border-yellow-600/20 bg-yellow-50/50 text-yellow-800"
        : "border-destructive/20 bg-destructive/10 text-destructive",
      className
    )}>
      <div className="flex items-start gap-3">
        <Icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
        <div className="space-y-1">
          {title && (
            <h3 className="font-medium leading-none tracking-tight">
              {title}
            </h3>
          )}
          <p className="text-sm [&:not(:first-child)]:mt-2">
            {message}
          </p>
        </div>
      </div>
    </div>
  )
}

export function ErrorFull({ 
  title = "Something went wrong", 
  message,
  variant 
}: Omit<ErrorProps, "className">) {
  return (
    <div className="flex items-center justify-center min-h-[200px] p-6">
      <Error 
        title={title} 
        message={message} 
        variant={variant}
        className="w-full max-w-md"
      />
    </div>
  )
}
