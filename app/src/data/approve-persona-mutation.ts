import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

export function useApprovePersonaMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      simulationId,
      personaId,
    }: {
      projectId: string;
      simulationId: string;
      personaId: string;
    }) => {
      return client.simulations.personas.approve(
        projectId,
        simulationId,
        personaId,
      );
    },
  });
}
