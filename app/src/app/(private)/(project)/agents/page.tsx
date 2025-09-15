import type * as React from "react";
import { redirect } from "next/navigation";

import { getProjectId } from "@/lib/cookies.server";

import { AgentsSection } from "./_components/agents-section";
import { CreateAgentDialog } from "./_components/create-agent-dialog";

export default async function Page(): Promise<React.JSX.Element> {
  const projectId = await getProjectId();

  if (!projectId) {
    redirect("/projects");
  }

  return (
    <main className="flex-1 flex flex-col py-6">
      <div className="max-w-7xl mx-auto w-full flex-1 flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div className="text-3xl font-bold">Agents</div>
          <CreateAgentDialog projectId={projectId} />
        </div>
        <AgentsSection projectId={projectId} />
      </div>
    </main>
  );
}
