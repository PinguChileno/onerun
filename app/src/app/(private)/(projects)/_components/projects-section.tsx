"use client";

import type * as React from "react";
import { Waveform } from "ldrs/react";
import { useRouter } from "next/navigation";

import { Card, CardContent } from "@/components/ui/card";
import { useListProjectsQuery } from "@/data/list-projects-query";
import type { Project } from "@/lib/api/resources/projects";
import { setProjectId } from "@/lib/cookies";
import { useCurrentProjectStore } from "@/stores/current-project-store";

import { ProjectCard } from "./project-card";

export function ProjectsSection(): React.JSX.Element {
  const router = useRouter();
  const { setCurrentProject } = useCurrentProjectStore();

  const { data, error, isLoading } = useListProjectsQuery();

  const handleSelect = (project: Project) => {
    setProjectId(project.id);
    setCurrentProject(project);
    router.push("/agents");
  };

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const projects = data?.data ?? [];

    if (!projects.length) {
      return <Empty />;
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onSelect={handleSelect}
          />
        ))}
      </div>
    );
  };

  return <div>{renderContent()}</div>;
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
        <div className="text-center text-muted-foreground">No projects yet</div>
      </CardContent>
    </Card>
  );
}
