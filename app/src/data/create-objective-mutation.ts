import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ObjectiveCreateParams } from "@/lib/api/resources/objectives";

export function useCreateObjectiveMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      params,
    }: {
      projectId: string;
      params: ObjectiveCreateParams;
    }) => {
      return client.objectives.create(projectId, params);
    },
  });
}
