import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ObjectiveUpdateParams } from "@/lib/api/resources/objectives";

export function useUpdateObjectiveMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      objectiveId,
      params,
    }: {
      projectId: string;
      objectiveId: string;
      params: ObjectiveUpdateParams;
    }) => {
      return client.objectives.update(projectId, objectiveId, params);
    },
  });
}
