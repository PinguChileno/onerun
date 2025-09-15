import { APIResource } from "../resource";
import type { Pagination } from "../types";

export type Agent = {
  id: string;
  created_at: string;
  description: string | null;
  name: string;
  project_id: string;
  total_simulations?: number;
  updated_at: string;
};

export type AgentCreateParams = {
  description?: string | null;
  name: string;
};

export type AgentUpdateParams = {
  description?: string | null;
  name?: string | null;
};

export type AgentListParams = {
  limit?: number;
  name?: string;
  offset?: number;
  sort_by?: "created_at" | "updated_at";
  sort_dir?: "asc" | "desc";
};

export class Agents extends APIResource {
  async create(projectId: string, params: AgentCreateParams): Promise<Agent> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/agents?${searchParams.toString()}`;

    return this._client.request<Agent>(url, {
      method: "POST",
      body: params,
      auth: true,
    });
  }

  async list(
    projectId: string,
    params: AgentListParams,
  ): Promise<Pagination<Agent>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    if (params.name) {
      searchParams.append("name", params.name);
    }

    if (params.sort_by) {
      searchParams.append("sort_by", params.sort_by);
    }

    if (params.sort_dir) {
      searchParams.append("sort_dir", params.sort_dir);
    }

    const url = `/v1/agents?${searchParams.toString()}`;

    return this._client.request<Pagination<Agent>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async get(projectId: string, agentId: string): Promise<Agent> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/agents/${agentId}?${searchParams.toString()}`;

    return this._client.request<Agent>(url, {
      method: "GET",
      auth: true,
    });
  }

  async update(
    projectId: string,
    agentId: string,
    params: AgentUpdateParams,
  ): Promise<Agent> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/agents/${agentId}?${searchParams.toString()}`;

    return this._client.request<Agent>(url, {
      method: "PATCH",
      body: params,
      auth: true,
    });
  }
}
