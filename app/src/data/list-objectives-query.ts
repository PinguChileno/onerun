import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ObjectiveListParams } from "@/lib/api/resources/objectives";

import { queryKeys } from "./query-keys";

export function useListObjectivesQuery(
  projectId: string,
  params: ObjectiveListParams = {},
) {
  return useQuery({
    queryKey: queryKeys.objectives.list(projectId, params),
    queryFn: () => {
      return client.objectives.list(projectId, params);
    },
  });
}
