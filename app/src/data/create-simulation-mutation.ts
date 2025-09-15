import { useMutation } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { SimulationCreateParams } from "@/lib/api/resources/simulations";

export function useCreateSimulationMutation() {
  return useMutation({
    mutationFn: ({
      projectId,
      params,
    }: {
      projectId: string;
      params: SimulationCreateParams;
    }) => {
      return client.simulations.create(projectId, params);
    },
  });
}
