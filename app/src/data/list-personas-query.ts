import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { PersonaListParams } from "@/lib/api/resources/simulations/personas";

import { queryKeys } from "./query-keys";

export function useListPersonasQuery(
  projectId: string,
  simulationId: string,
  params: PersonaListParams = {},
) {
  return useQuery({
    queryKey: queryKeys.simulations.personas.list(
      projectId,
      simulationId,
      params,
    ),
    queryFn: () => {
      return client.simulations.personas.list(projectId, simulationId, params);
    },
  });
}
