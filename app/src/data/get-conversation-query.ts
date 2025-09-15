import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

import { queryKeys } from "./query-keys";

export function useGetConversationQuery(
  projectId: string,
  simulationId: string,
  conversationId: string,
) {
  return useQuery({
    queryKey: queryKeys.simulations.conversations.get(
      projectId,
      simulationId,
      conversationId,
    ),
    queryFn: () => {
      return client.simulations.conversations.get(
        projectId,
        simulationId,
        conversationId,
      );
    },
  });
}
