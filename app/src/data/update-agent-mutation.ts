import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { AgentUpdateParams } from "@/lib/api/resources/agents";

export function useUpdateAgentMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      agentId,
      params,
    }: {
      projectId: string;
      agentId: string;
      params: AgentUpdateParams;
    }) => {
      return client.agents.update(projectId, agentId, params);
    },
  });
}
