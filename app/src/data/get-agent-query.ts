import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

import { queryKeys } from "./query-keys";

export function useGetAgentQuery(projectId: string, agentId: string) {
  return useQuery({
    queryKey: queryKeys.agents.get(projectId, agentId),
    queryFn: () => {
      return client.agents.get(projectId, agentId);
    },
  });
}
