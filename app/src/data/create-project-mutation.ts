import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ProjectCreateParams } from "@/lib/api/resources/projects";

export function useCreateProjectMutation() {
  return useMutation({
    mutationFn: (params: ProjectCreateParams) => {
      return client.projects.create(params);
    },
  });
}
