import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

import { queryKeys } from "./query-keys";

export function useListConversationItemsQuery(
  projectId: string,
  simulationId: string,
  conversationId: string,
) {
  return useQuery({
    queryKey: queryKeys.simulations.conversations.items(
      projectId,
      simulationId,
      conversationId,
    ),
    queryFn: () => {
      return client.simulations.conversations.listItems(
        projectId,
        simulationId,
        conversationId,
      );
    },
  });
}
