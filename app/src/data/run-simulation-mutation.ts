import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

export function useRunSimulationMutation() {
  return useMutation({
    mutationFn: async ({
      projectId,
      simulationId,
    }: {
      projectId: string;
      simulationId: string;
    }) => {
      return client.simulations.run(simulationId, projectId);
    },
  });
}
