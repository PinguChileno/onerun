import type * as React from "react";
import Link from "next/link";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Agent } from "@/lib/api/resources/agents";

export interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps): React.JSX.Element {
  return (
    <Link className="flex flex-col" href={`/agents/${agent.id}`}>
      <Card className="flex-1 cursor-pointer transition-shadow hover:shadow-md hover:bg-card/90">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Avatar className="bg-background-3 h-10 w-10">
              <AvatarFallback className="bg-background-3 text-sm text-foreground font-medium uppercase">
                {agent.name.slice(0, 2)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 flex flex-col gap-2 min-w-0">
              <div>
                <CardTitle className="text-lg">{agent.name}</CardTitle>
                <div className="text-sm text-muted-foreground">
                  ID: {agent.id}
                </div>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent className="flex flex-col gap-2">
          <div>
            <div>
              <div className="text-sm text-muted-foreground">
                All Simulations
              </div>
              <div className="font-semibold">{agent.total_simulations}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
