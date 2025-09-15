import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

import { queryKeys } from "./query-keys";

export function useGetSimulationQuery(projectId: string, simulationId: string) {
  return useQuery({
    queryKey: queryKeys.simulations.get(projectId, simulationId),
    queryFn: () => {
      return client.simulations.get(projectId, simulationId);
    },
  });
}
