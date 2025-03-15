"use client"

import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface LoadingProps {
  className?: string;
  size?: "default" | "sm" | "lg";
  center?: boolean;
  text?: string;
}

const sizeClasses = {
  default: "h-6 w-6",
  sm: "h-4 w-4",
  lg: "h-8 w-8"
}

export function Loading({ 
  className, 
  size = "default",
  center = false,
  text
}: LoadingProps) {
  const content = (
    <>
      <Loader2 className={cn(
        "animate-spin text-muted-foreground",
        sizeClasses[size],
        className
      )} />
      {text && (
        <p className="text-muted-foreground text-sm">{text}</p>
      )}
    </>
  )

  if (center) {
    return (
      <div className="flex flex-col items-center justify-center gap-2 h-full min-h-[100px]">
        {content}
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2">
      {content}
    </div>
  )
}

export function LoadingPage() {
  return (
    <div className="flex items-center justify-center h-screen">
      <Loading size="lg" text="Loading..." />
    </div>
  )
}

export function LoadingInline() {
  return <Loading size="sm" />
}
