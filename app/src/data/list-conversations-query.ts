import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ConversationListParams } from "@/lib/api/resources/simulations/conversations";

import { queryKeys } from "./query-keys";

export function useListConversationsQuery(
  projectId: string,
  simulationId: string,
  params: ConversationListParams = {},
) {
  return useQuery({
    queryKey: queryKeys.simulations.conversations.list(
      projectId,
      simulationId,
      params,
    ),
    queryFn: () => {
      return client.simulations.conversations.list(
        projectId,
        simulationId,
        params,
      );
    },
  });
}
