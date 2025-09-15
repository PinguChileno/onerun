import type * as React from "react";
import Link from "next/link";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Simulation } from "@/lib/api/resources/simulations";

import { SimulationStatusBadge } from "./simulation-status-badge";

export interface SimulationCardProps {
  simulation: Simulation;
}

export function SimulationCard({
  simulation,
}: SimulationCardProps): React.JSX.Element {
  return (
    <Link
      href={`/agents/${simulation.agent_id}/simulations/${simulation.id}`}
      className="flex flex-col"
    >
      <Card className="flex-1 cursor-pointer transition-shadow hover:shadow-md hover:bg-card/90">
        <CardHeader>
          <div className="flex justify-between items-start">
            <CardTitle className="text-base">{simulation.name}</CardTitle>
            <SimulationStatusBadge status={simulation.status} />
          </div>
          <CardDescription className="line-clamp-2">
            {simulation.scenario}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-2 text-sm text-muted-foreground">
            <div className="flex justify-between">
              <span>Target Personas:</span>
              <span>{simulation.target_personas}</span>
            </div>
            <div className="flex justify-between">
              <span>Conversations:</span>
              <span>{simulation.target_conversations}</span>
            </div>
            <div className="flex justify-between">
              <span>Auto-approve:</span>
              <span>{simulation.auto_approve ? "Yes" : "No"}</span>
            </div>
            <div className="flex justify-between">
              <span>Created:</span>
              <span>
                {new Date(simulation.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
