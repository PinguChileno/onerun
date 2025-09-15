import { APIResource } from "../../resource";
import type { Pagination } from "../../types";
import type { Objective } from "../objectives";
import type { Persona } from "./personas";

export type ConversationStatus =
  | "ended"
  | "failed"
  | "in_progress"
  | "pending"
  | "queued";

export type EvaluationStatus =
  | "completed"
  | "failed"
  | "in_progress"
  | "not_applicable"
  | "pending"
  | "queued";

export type ConversationEvaluation = {
  id: string;
  conversation_id: string;
  objective: Objective | null;
  objective_id: string;
  score: number;
  reason: string;
};

export type ConversationItem = {
  id: string;
  conversation_id: string;
  type: string;
  role: "user" | "assistant";
  content: Array<{
    type: string;
    text: string;
  }>;
  created_at: string;
};

export type Conversation = {
  id: string;
  created_at: string;
  end_reason: string | null;
  evaluation_status: EvaluationStatus;
  evaluations: ConversationEvaluation[];
  persona: Persona | null;
  persona_id: string;
  seq_id: number;
  simulation_id: string;
  status: ConversationStatus;
};

export type ConversationListParams = {
  sort_by?: "created_at";
  sort_dir?: "asc" | "desc";
};

export class Conversations extends APIResource {
  async list(
    projectId: string,
    simulationId: string,
    params: ConversationListParams,
  ): Promise<Pagination<Conversation>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    if (params.sort_by) {
      searchParams.append("sort_by", params.sort_by);
    }

    if (params.sort_dir) {
      searchParams.append("sort_dir", params.sort_dir);
    }

    const url = `/v1/simulations/${simulationId}/conversations?${searchParams.toString()}`;

    return this._client.request<Pagination<Conversation>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async get(
    projectId: string,
    simulationId: string,
    conversationId: string,
  ): Promise<Conversation> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/conversations/${conversationId}?${searchParams.toString()}`;

    return this._client.request<Conversation>(url, {
      method: "GET",
      auth: true,
    });
  }

  async listItems(
    projectId: string,
    simulationId: string,
    conversationId: string,
  ): Promise<Pagination<ConversationItem>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/simulations/${simulationId}/conversations/${conversationId}/items?${searchParams.toString()}`;

    return this._client.request<Pagination<ConversationItem>>(url, {
      method: "POST",
      auth: true,
    });
  }
}
