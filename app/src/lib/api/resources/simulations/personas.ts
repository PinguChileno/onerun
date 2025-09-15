import { APIResource } from "../../resource";
import type { Pagination } from "../../types";

export type ApprovalStatus = "pending" | "approved" | "rejected";

export type PersonaAttributes = {
  age_group: string;
  education: string;
  occupation: string;
  economic_status: string;
  personality_traits: string;
  values: string;
  habits: string;
  interests: string;
  speech_style: string;
  speech_patterns: string;
  typical_behavior: string;
  stress_triggers: string;
  stress_reactions: string;
  version: "v1";
};

export type Persona = {
  id: string;
  approval_status: ApprovalStatus;
  attributes: PersonaAttributes;
  auto_approve: boolean;
  created_at: string;
  metadata: Record<string, unknown>;
  purpose: string;
  seq_id: number;
  simulation_id: string;
  story: string;
  summary: string;
  updated_at: string;
};

export type PersonaListParams = {
  approval_status?: ApprovalStatus;
  sort_by?: "name" | "created_at";
  sort_dir?: "asc" | "desc";
};

export class Personas extends APIResource {
  async list(
    projectId: string,
    simulationId: string,
    params: PersonaListParams,
  ): Promise<Pagination<Persona>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    if (params.approval_status) {
      searchParams.append("approval_status", params.approval_status);
    }

    if (params.sort_by) {
      searchParams.append("sort_by", params.sort_by);
    }

    if (params.sort_dir) {
      searchParams.append("sort_dir", params.sort_dir);
    }

    const url = `/v1/simulations/${simulationId}/personas?${searchParams.toString()}`;

    return this._client.request<Pagination<Persona>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async approve(
    projectId: string,
    simulationId: string,
    personaId: string,
  ): Promise<{ message: string }> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/personas/${personaId}/approve?${searchParams.toString()}`;

    return this._client.request<{ message: string }>(url, {
      method: "POST",
      auth: true,
    });
  }

  async reject(
    projectId: string,
    simulationId: string,
    personaId: string,
  ): Promise<{ message: string }> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/personas/${personaId}/reject?${searchParams.toString()}`;

    return this._client.request<{ message: string }>(url, {
      method: "POST",
      auth: true,
    });
  }
}
