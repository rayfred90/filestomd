"use client"

import { cn } from "@/lib/utils"

interface HeadingProps {
  title: string;
  description?: string;
  className?: string;
}

export function Heading({ 
  title, 
  description, 
  className 
}: HeadingProps) {
  return (
    <div className={cn("flex flex-col gap-1", className)}>
      <h1 className="text-2xl font-semibold tracking-tight">
        {title}
      </h1>
      {description && (
        <p className="text-sm text-muted-foreground">
          {description}
        </p>
      )}
    </div>
  )
}

export function PageHeading({ 
  title, 
  description, 
  className 
}: HeadingProps) {
  return (
    <div className={cn("flex flex-col gap-2 mb-8", className)}>
      <h1 className="text-4xl font-bold">
        {title}
      </h1>
      {description && (
        <p className="text-lg text-muted-foreground">
          {description}
        </p>
      )}
    </div>
  )
}
