import type * as React from "react";
import { redirect } from "next/navigation";

import { getProjectId } from "@/lib/cookies.server";

import { SimulationDetails } from "./_components/simulation-details";

export interface PageProps {
  params: Promise<{
    agentId: string;
    simulationId: string;
  }>;
}

export default async function Page({
  params,
}: PageProps): Promise<React.JSX.Element> {
  const { agentId, simulationId } = await params;
  const projectId = await getProjectId();

  if (!projectId) {
    redirect("/projects");
  }

  return (
    <main className="flex-1 flex flex-col">
      <div className="max-w-7xl mx-auto w-full flex flex-col">
        <SimulationDetails
          agentId={agentId}
          simulationId={simulationId}
          projectId={projectId}
        />
      </div>
    </main>
  );
}
