import type * as React from "react";

import { StatusBadge } from "@/components/ui/status-badge";
import type { EvaluationStatus } from "@/lib/api/resources/simulations/conversations";

export interface EvaluationStatusBadgeProps {
  status: EvaluationStatus;
}

export function EvaluationStatusBadge({
  status,
}: EvaluationStatusBadgeProps): React.JSX.Element {
  const statusMap: Record<
    EvaluationStatus,
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
    completed: { variant: "completed", label: "Completed" },
    failed: { variant: "failed", label: "Failed" },
    in_progress: { variant: "in_progress", label: "In Progress" },
    not_applicable: { variant: "in_progress", label: "N/A" },
    pending: { variant: "in_progress", label: "Pending" },
    queued: { variant: "queued", label: "Queued" },
  };

  const config = statusMap[status] || {
    variant: "in_progress" as const,
    label: "Unknown",
  };

  return <StatusBadge variant={config.variant}>{config.label}</StatusBadge>;
}
