"use client"

import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset",
  {
    variants: {
      variant: {
        default:
          "bg-primary/10 text-primary ring-primary/20",
        secondary:
          "bg-secondary text-secondary-foreground ring-secondary/20",
        success:
          "bg-green-50 text-green-700 ring-green-600/20",
        destructive:
          "bg-destructive/10 text-destructive ring-destructive/20",
        outline:
          "text-foreground ring-border",
        warning:
          "bg-yellow-50 text-yellow-800 ring-yellow-600/20",
        info:
          "bg-blue-50 text-blue-700 ring-blue-700/20",
        pending:
          "bg-orange-50 text-orange-700 ring-orange-600/20"
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export function StatusBadge({ 
  status 
}: { 
  status: 'pending' | 'processing' | 'completed' | 'failed' 
}) {
  const variants = {
    pending: 'warning',
    processing: 'info',
    completed: 'success',
    failed: 'destructive',
  } as const

  return (
    <Badge variant={variants[status]}>
      {status}
    </Badge>
  )
}

export function FileBadge({ 
  type 
}: { 
  type: string 
}) {
  return (
    <Badge variant="outline" className="font-mono uppercase">
      {type}
    </Badge>
  )
}
