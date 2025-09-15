import type * as React from "react";
import { redirect } from "next/navigation";

import { getProjectId } from "@/lib/cookies.server";

import { AgentDetails } from "./_components/agent-details";

export interface PageProps {
  params: Promise<{
    agentId: string;
  }>;
}

export default async function Page({
  params,
}: PageProps): Promise<React.JSX.Element> {
  const { agentId } = await params;
  const projectId = await getProjectId();

  if (!projectId) {
    redirect("/projects");
  }

  return (
    <main className="flex-1 flex flex-col">
      <div className="max-w-7xl mx-auto w-full flex-1 flex flex-col">
        <AgentDetails agentId={agentId} projectId={projectId} />
      </div>
    </main>
  );
}
