import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { AgentListParams } from "@/lib/api/resources/agents";

import { queryKeys } from "./query-keys";

export function useListAgentsQuery(
  projectId: string,
  params: AgentListParams = {},
) {
  return useQuery({
    queryKey: queryKeys.agents.list(projectId, params),
    queryFn: () => {
      return client.agents.list(projectId, params);
    },
  });
}
