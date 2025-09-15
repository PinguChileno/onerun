"use client";

import type * as React from "react";
import { Waveform } from "ldrs/react";

import { Card, CardContent } from "@/components/ui/card";
import { useListAgentsQuery } from "@/data/list-agents-query";
import { useAgentFiltersStore } from "@/stores/agent-filters-store";

import { AgentCard } from "./agent-card";
import { AgentsIntro } from "./agents-intro";

export interface AgentsSectionProps {
  projectId: string;
}

export function AgentsSection({
  projectId,
}: AgentsSectionProps): React.JSX.Element {
  const { filters } = useAgentFiltersStore();

  const { data, error, isLoading } = useListAgentsQuery(projectId, {
    name: filters.name || undefined,
    sort_by: filters.sortBy,
    sort_dir: filters.sortDir,
  });

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const agents = data?.data ?? [];

    if (!agents.length) {
      const filtered = Boolean(filters.name);

      if (!filtered) {
        return <AgentsIntro />;
      }

      return <Empty />;
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    );
  };

  return renderContent();
}

function Loading(): React.JSX.Element {
  return (
    <div className="flex justify-center py-12">
      <Waveform size="35" stroke="3.5" speed="1" color="white" />
    </div>
  );
}

interface ErrorDisplayProps {
  message: string;
}

function ErrorDisplay({ message }: ErrorDisplayProps): React.JSX.Element {
  return (
    <div className="py-12">
      <p className="text-center text-muted-foreground">{message}</p>
    </div>
  );
}

function Empty(): React.JSX.Element {
  return (
    <Card>
      <CardContent className="py-12">
        <div className="text-center text-muted-foreground">No agents yet</div>
      </CardContent>
    </Card>
  );
}
