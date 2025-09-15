"use client";

import type * as React from "react";
import { Waveform } from "ldrs/react";
import { PlusIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useListSimulationsQuery } from "@/data/list-simulations-query";

import { SimulationCard } from "./simulation-card";
import { SimulationsIntro } from "./simulations-intro";

export interface SimulationsSectionProps {
  agentId: string;
  projectId: string;
  onCreate: () => void;
}

export function SimulationsSection({
  agentId,
  projectId,
  onCreate,
}: SimulationsSectionProps): React.JSX.Element {
  const { data, error, isLoading } = useListSimulationsQuery(projectId, {
    agent_id: agentId,
  });

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const simulations = data?.data ?? [];

    if (!simulations.length) {
      return <SimulationsIntro />;
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {simulations.map((simulation) => (
          <SimulationCard key={simulation.id} simulation={simulation} />
        ))}
      </div>
    );
  };

  return (
    <div className="flex-1 flex flex-col gap-4 py-6">
      <div className="flex justify-between items-start">
        <div>
          <div className="text-xl font-bold">Simulations</div>
        </div>
        <Button className="cursor-pointer" onClick={onCreate}>
          <PlusIcon />
          New Simulation
        </Button>
      </div>
      {renderContent()}
    </div>
  );
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
