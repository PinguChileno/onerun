import type { AgentListParams } from "@/lib/api/resources/agents";
import type { ObjectiveListParams } from "@/lib/api/resources/objectives";
import type { ProjectListParams } from "@/lib/api/resources/projects";
import type { SimulationListParams } from "@/lib/api/resources/simulations";
import type { ConversationListParams } from "@/lib/api/resources/simulations/conversations";
import type { PersonaListParams } from "@/lib/api/resources/simulations/personas";

export const queryKeys = {
  projects: {
    all: () => ["projects"],
    list: (params: ProjectListParams) => ["projects", params],
    get: (projectId: string) => ["projects", projectId],
  },
  agents: {
    all: (projectId: string) => ["projects", projectId, "agents"],
    list: (projectId: string, params: AgentListParams) => [
      "projects",
      projectId,
      "agents",
      params,
    ],
    get: (projectId: string, agentId: string) => [
      "projects",
      projectId,
      "agents",
      agentId,
    ],
  },
  objectives: {
    all: (projectId: string) => ["projects", projectId, "objectives"],
    list: (projectId: string, params: ObjectiveListParams) => [
      "projects",
      projectId,
      "objectives",
      params,
    ],
    get: (projectId: string, objectiveId: string) => [
      "projects",
      projectId,
      "objectives",
      objectiveId,
    ],
  },
  simulations: {
    all: (projectId: string) => ["projects", projectId, "simulations"],
    list: (projectId: string, params: SimulationListParams) => [
      "projects",
      projectId,
      "simulations",
      params,
    ],
    get: (projectId: string, simulationId: string) => [
      "projects",
      projectId,
      "simulations",
      simulationId,
    ],
    personas: {
      all: (projectId: string, simulationId: string) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "personas",
      ],
      list: (
        projectId: string,
        simulationId: string,
        params: PersonaListParams,
      ) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "personas",
        params,
      ],
      get: (projectId: string, simulationId: string, personaId: string) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "personas",
        personaId,
      ],
    },
    conversations: {
      all: (projectId: string, simulationId: string) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "conversations",
      ],
      list: (
        projectId: string,
        simulationId: string,
        params: ConversationListParams,
      ) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "conversations",
        params,
      ],
      get: (
        projectId: string,
        simulationId: string,
        conversationId: string,
      ) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "conversations",
        conversationId,
      ],
      items: (
        projectId: string,
        simulationId: string,
        conversationId: string,
      ) => [
        "projects",
        projectId,
        "simulations",
        simulationId,
        "conversations",
        conversationId,
        "items",
      ],
    },
  },
} as const;
