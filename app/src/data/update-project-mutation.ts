import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ProjectUpdateParams } from "@/lib/api/resources/projects";

export function useUpdateProjectMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      params,
    }: {
      projectId: string;
      params: ProjectUpdateParams;
    }) => {
      return client.projects.update(projectId, params);
    },
  });
}
