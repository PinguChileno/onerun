import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { AgentCreateParams } from "@/lib/api/resources/agents";

export function useCreateAgentMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      params,
    }: {
      projectId: string;
      params: AgentCreateParams;
    }) => {
      return client.agents.create(projectId, params);
    },
  });
}
