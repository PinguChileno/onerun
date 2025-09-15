import type * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import {
  CheckCircleIcon,
  CircleIcon,
  EllipsisIcon,
  TimerIcon,
  TriangleAlertIcon,
} from "lucide-react";

import { cn } from "@/lib/utils";

type StatusBadgeVariant =
  | "completed"
  | "in_progress"
  | "failed"
  | "partial_failed"
  | "queued";

const statusBadgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2 py-1 text-xs font-semibold text-foreground",
  {
    variants: {
      variant: {
        completed: "",
        in_progress: "",
        failed: "",
        partial_failed: "",
        queued: "",
      },
    },
    defaultVariants: {
      variant: "completed",
    },
  },
);

const iconMap = {
  completed: CheckCircleIcon,
  in_progress: EllipsisIcon,
  failed: TriangleAlertIcon,
  partial_failed: CircleIcon,
  queued: TimerIcon,
} as const;

const iconColorMap = {
  completed: "text-green-500",
  in_progress: "text-primary",
  failed: "text-destructive",
  partial_failed: "text-orange-500",
  queued: "text-yellow-500",
} as const;

export interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof statusBadgeVariants> {
  children: React.ReactNode;
}

function StatusBadge({
  className,
  variant = "completed",
  children,
  ...props
}: StatusBadgeProps) {
  const Icon = iconMap[variant as StatusBadgeVariant] ?? EllipsisIcon;
  const iconColor =
    iconColorMap[variant as StatusBadgeVariant] ?? "text-gray-500";

  return (
    <div className={cn(statusBadgeVariants({ variant }), className)} {...props}>
      <Icon className={cn("h-4 w-4", iconColor)} />
      {children}
    </div>
  );
}

StatusBadge.displayName = "StatusBadge";

export { StatusBadge, statusBadgeVariants };
