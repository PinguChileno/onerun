import { useQuery } from "@tanstack/react-query";

import { client } from "@/lib/api/client";
import type { ProjectListParams } from "@/lib/api/resources/projects";

import { queryKeys } from "./query-keys";

export function useListProjectsQuery(params: ProjectListParams = {}) {
  return useQuery({
    queryKey: queryKeys.projects.list(params),
    queryFn: () => {
      return client.projects.list(params);
    },
  });
}
