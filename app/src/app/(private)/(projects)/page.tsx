import type * as React from "react";

import { CreateProjectDialog } from "./_components/create-project-dialog";
import { ProjectNavbar } from "./_components/projects-navbar";
import { ProjectsSection } from "./_components/projects-section";

export default function Page(): React.JSX.Element {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <ProjectNavbar />
      <main className="flex-1 flex flex-col py-6">
        <div className="max-w-7xl mx-auto w-full flex flex-col gap-6">
          <div className="flex justify-between items-center">
            <div className="text-3xl font-bold">Projects</div>
            <CreateProjectDialog />
          </div>
          <ProjectsSection />
        </div>
      </main>
    </div>
  );
}
