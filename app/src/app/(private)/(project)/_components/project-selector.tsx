"use client";

import type * as React from "react";
import { ChevronDownIcon, FolderIcon, PlusIcon } from "lucide-react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useListProjectsQuery } from "@/data/list-projects-query";
import type { Project } from "@/lib/api/resources/projects";
import { setProjectId } from "@/lib/cookies";
import { useCurrentProjectStore } from "@/stores/current-project-store";

export function ProjectSelector(): React.JSX.Element {
  const router = useRouter();
  const { data: projectsData, isLoading } = useListProjectsQuery();
  const { currentProject, setCurrentProject } = useCurrentProjectStore();

  const projects = projectsData?.data || [];

  const handleProjectChange = (project: Project) => {
    setProjectId(project.id);
    setCurrentProject(project);
    router.refresh();
  };

  const handleNewProject = () => {
    // Navigate back to projects page to create new project
    router.push("/");
  };

  if (isLoading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <FolderIcon className="h-4 w-4" />
        Loading...
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <FolderIcon className="h-4 w-4" />
        No projects
      </div>
    );
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button className="w-[200px] justify-between bg-background/80 hover:bg-background text-foreground border cursor-pointer">
          <div className="flex items-center gap-2">
            <FolderIcon className="h-4 w-4 text-muted-foreground" />
            {currentProject?.name || "Select project"}
          </div>
          <ChevronDownIcon className="h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-1" align="start">
        <div className="flex flex-col gap-1">
          {projects.map((project) => (
            <Button
              key={project.id}
              variant={
                currentProject?.id === project.id ? "secondary" : "ghost"
              }
              className="cursor-pointer w-full justify-start h-8 px-2"
              onClick={() => handleProjectChange(project)}
            >
              <div className="flex items-center gap-2">
                <FolderIcon className="h-4 w-4" />
                {project.name}
                {currentProject?.id === project.id && (
                  <span className="ml-auto text-xs text-muted-foreground">
                    Current
                  </span>
                )}
              </div>
            </Button>
          ))}
          <div className="border-t pt-1">
            <Button
              variant="ghost"
              className="cursor-pointer w-full justify-start h-8 px-2"
              onClick={handleNewProject}
            >
              <PlusIcon />
              Manage Projects
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
