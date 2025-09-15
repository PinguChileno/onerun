import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";

import { queryKeys } from "./query-keys";

export function useGetProjectQuery(projectId: string) {
  return useQuery({
    queryKey: queryKeys.projects.get(projectId),
    queryFn: () => {
      return client.projects.get(projectId);
    },
  });
}
