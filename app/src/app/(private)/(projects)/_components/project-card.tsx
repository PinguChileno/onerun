import type * as React from "react";
import { FolderIcon } from "lucide-react";

import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import type { Project } from "@/lib/api/resources/projects";

export interface ProjectCardProps {
  project: Project;
  onSelect?: (project: Project) => void;
}

export function ProjectCard({
  project,
  onSelect,
}: ProjectCardProps): React.JSX.Element {
  return (
    <Card
      key={project.id}
      className="hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => onSelect?.(project)}
    >
      <CardHeader>
        <div className="flex items-start space-x-3">
          <div className="p-2 bg-primary/10 rounded-lg">
            <FolderIcon className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <CardTitle className="text-lg">{project.name}</CardTitle>
          </div>
        </div>
      </CardHeader>
    </Card>
  );
}
