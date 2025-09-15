"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";
import { useRouter } from "next/navigation";

import { useListProjectsQuery } from "@/data/list-projects-query";
import { getProjectId, removeProjectId } from "@/lib/cookies";
import { useCurrentProjectStore } from "@/stores/current-project-store";

import { ProjectNavbar } from "./_components/project-navbar";

export interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): React.JSX.Element {
  const router = useRouter();
  const { currentProject, setCurrentProject } = useCurrentProjectStore();
  const { data, isLoading } = useListProjectsQuery();

  React.useEffect(() => {
    const projectId = getProjectId();

    if (!projectId) {
      setCurrentProject(null);
      router.push("/");
      return;
    }

    if (isLoading) {
      return;
    }

    const project = data?.data.find((project) => project.id === projectId);

    if (!project) {
      removeProjectId();
      setCurrentProject(null);
      router.push("/");
      return;
    }

    setCurrentProject(project);
  }, [data, isLoading, setCurrentProject, router]);

  if (!currentProject) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Waveform size="35" stroke="3.5" speed="1" color="white" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <ProjectNavbar />
      {children}
    </div>
  );
}
