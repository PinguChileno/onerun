import type * as React from "react";
import { redirect } from "next/navigation";

import { getProjectId } from "@/lib/cookies.server";

import { CreateObjectiveDialog } from "./_components/create-objective-dialog";
import { ObjectivesTable } from "./_components/objectives-table";

export default async function Page(): Promise<React.JSX.Element> {
  const projectId = await getProjectId();

  if (!projectId) {
    redirect("/projects");
  }

  return (
    <main className="flex-1 flex flex-col py-6">
      <div className="max-w-7xl mx-auto w-full flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div className="text-2xl font-bold">Objectives</div>
          <CreateObjectiveDialog projectId={projectId} />
        </div>
        <ObjectivesTable projectId={projectId} />
      </div>
    </main>
  );
}
