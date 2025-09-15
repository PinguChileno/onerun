import type * as React from "react";

import { StatusBadge } from "@/components/ui/status-badge";
import type { SimulationStatus } from "@/lib/api/resources/simulations";

export interface SimulationStatusBadgeProps {
  status: SimulationStatus;
}

export function SimulationStatusBadge({
  status,
}: SimulationStatusBadgeProps): React.JSX.Element {
  const statusMap: Record<
    SimulationStatus,
    {
      variant: "completed" | "in_progress" | "failed" | "partial_failed";
      label: string;
    }
  > = {
    canceled: { variant: "failed", label: "Canceled" },
    completed: { variant: "completed", label: "Completed" },
    expired: { variant: "failed", label: "Expired" },
    failed: { variant: "failed", label: "Failed" },
    in_progress: { variant: "in_progress", label: "In Progress" },
    pending: { variant: "in_progress", label: "Pending" },
    queued: { variant: "in_progress", label: "Queued" },
  };

  const config = statusMap[status] || {
    variant: "in_progress" as const,
    label: "Unknown",
  };

  return <StatusBadge variant={config.variant}>{config.label}</StatusBadge>;
}
