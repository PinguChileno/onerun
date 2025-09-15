import type { Client } from "../../client";
import { APIResource } from "../../resource";
import type { Pagination } from "../../types";
import type { Agent } from "../agents";
import type { Objective } from "../objectives";
import { Conversations } from "./conversations";
import { Personas } from "./personas";

export type SimulationStatus =
  | "canceled"
  | "completed"
  | "expired"
  | "failed"
  | "in_progress"
  | "pending"
  | "queued";

export type Simulation = {
  id: string;
  agent: Agent | null;
  agent_id: string;
  auto_approve: boolean;
  created_at: string;
  expires_at: string | null;
  last_failure_reason?: string | null;
  max_turns: number;
  metadata?: Record<string, unknown> | null;
  name: string;
  objectives: Objective[];
  project_id: string;
  scenario: string;
  status: SimulationStatus;
  target_conversations: number;
  target_personas: number;
  updated_at: string;
};

export type SimulationCreateParams = {
  agent_id: string;
  auto_approve?: boolean;
  max_turns?: number;
  name: string;
  objective_ids?: string[];
  scenario: string;
  target_conversations: number;
  target_personas: number;
};

export type SimulationListParams = {
  agent_id?: string;
  sort_by?: "name" | "created_at" | "updated_at";
  sort_dir?: "asc" | "desc";
  status?: string;
};

export class Simulations extends APIResource {
  public conversations: Conversations;
  public personas: Personas;

  constructor(client: Client) {
    super(client);
    this.conversations = new Conversations(client);
    this.personas = new Personas(client);
  }

  async create(
    projectId: string,
    params: SimulationCreateParams,
  ): Promise<Simulation> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations?${searchParams.toString()}`;

    return this._client.request<Simulation>(url, {
      method: "POST",
      body: params,
      auth: true,
    });
  }

  async list(
    projectId: string,
    params: SimulationListParams,
  ): Promise<Pagination<Simulation>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    if (params.agent_id) {
      searchParams.append("agent_id", params.agent_id);
    }

    if (params.sort_by) {
      searchParams.append("sort_by", params.sort_by);
    }

    if (params.sort_dir) {
      searchParams.append("sort_dir", params.sort_dir);
    }

    if (params.status) {
      searchParams.append("status", params.status);
    }

    const url = `/v1/simulations?${searchParams.toString()}`;

    return this._client.request<Pagination<Simulation>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async get(projectId: string, simulationId: string): Promise<Simulation> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}?${searchParams.toString()}`;

    return this._client.request<Simulation>(url, {
      method: "GET",
      auth: true,
    });
  }

  async run(projectId: string, simulationId: string): Promise<Simulation> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/run?${searchParams.toString()}`;

    return this._client.request<Simulation>(url, {
      method: "POST",
      auth: true,
    });
  }

  async cancel(projectId: string, simulationId: string): Promise<Simulation> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/cancel?${searchParams.toString()}`;

    return this._client.request<Simulation>(url, {
      method: "POST",
      auth: true,
    });
  }
}
