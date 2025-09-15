import type * as React from "react";

import { StatusBadge } from "@/components/ui/status-badge";
import type { ApprovalStatus } from "@/lib/api/resources/simulations/personas";

export interface ApprovalStatusBadgeProps {
  status: ApprovalStatus;
}

export function ApprovalStatusBadge({
  status,
}: ApprovalStatusBadgeProps): React.JSX.Element {
  const statusMap: Record<
    ApprovalStatus,
    {
      variant: "completed" | "failed" | "queued";
      label: string;
    }
  > = {
    approved: { variant: "completed", label: "Approved" },
    rejected: { variant: "failed", label: "Rejected" },
    pending: { variant: "queued", label: "Pending" },
  };

  const config = statusMap[status] || {
    variant: "queued" as const,
    label: "Unknown",
  };

  return <StatusBadge variant={config.variant}>{config.label}</StatusBadge>;
}
