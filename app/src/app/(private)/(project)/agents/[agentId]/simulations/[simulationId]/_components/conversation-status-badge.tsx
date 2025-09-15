"use client";

import type * as React from "react";

import { StatusBadge } from "@/components/ui/status-badge";
import type { ConversationStatus } from "@/lib/api/resources/simulations/conversations";

export interface ConversationStatusBadgeProps {
  status: ConversationStatus;
}

export function ConversationStatusBadge({
  status,
}: ConversationStatusBadgeProps): React.JSX.Element {
  const statusMap: Record<
    ConversationStatus,
    {
      variant:
        | "completed"
        | "in_progress"
        | "failed"
        | "partial_failed"
        | "queued";
      label: string;
    }
  > = {
    ended: { variant: "completed", label: "Ended" },
    failed: { variant: "failed", label: "Failed" },
    in_progress: { variant: "in_progress", label: "In Progress" },
    pending: { variant: "in_progress", label: "Pending" },
    queued: { variant: "queued", label: "Queued" },
  };

  const config = statusMap[status] || {
    variant: "in_progress" as const,
    label: "Unknown",
  };

  return <StatusBadge variant={config.variant}>{config.label}</StatusBadge>;
}
