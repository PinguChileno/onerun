import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

export function useCancelSimulationMutation() {
  return useMutation({
    mutationFn: async ({
      projectId,
      simulationId,
    }: {
      projectId: string;
      simulationId: string;
    }) => {
      return client.simulations.cancel(projectId, simulationId);
    },
  });
}
