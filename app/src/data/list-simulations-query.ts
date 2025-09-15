import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { SimulationListParams } from "@/lib/api/resources/simulations";

import { queryKeys } from "./query-keys";

export function useListSimulationsQuery(
  projectId: string,
  params: SimulationListParams = {},
) {
  return useQuery({
    queryKey: queryKeys.simulations.list(projectId, params),
    queryFn: () => {
      return client.simulations.list(projectId, params);
    },
  });
}
