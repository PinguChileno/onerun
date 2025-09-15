import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

export function useRejectPersonaMutation() {
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
      return client.simulations.personas.reject(
        projectId,
        simulationId,
        personaId,
      );
    },
  });
}
