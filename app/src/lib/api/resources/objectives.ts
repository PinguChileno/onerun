import { APIResource } from "../resource";
import type { Pagination } from "../types";

export type Objective = {
  id: string;
  created_at: string;
  criteria: string;
  name: string;
  project_id: string;
  updated_at: string;
};

export type ObjectiveCreateParams = {
  criteria: string;
  name: string;
};

export type ObjectiveUpdateParams = {
  criteria?: string | null;
  name?: string | null;
};

export type ObjectiveListParams = {
  limit?: number;
  offset?: number;
  sort_by?: "created_at";
  sort_dir?: "asc" | "desc";
};

export class Objectives extends APIResource {
  async create(
    projectId: string,
    params: ObjectiveCreateParams,
  ): Promise<Objective> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/objectives?${searchParams.toString()}`;

    return this._client.request<Objective>(url, {
      method: "POST",
      body: params,
      auth: true,
    });
  }

  async list(
    projectId: string,
    params: ObjectiveListParams,
  ): Promise<Pagination<Objective>> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    if (params.limit) {
      searchParams.append("limit", params.limit.toString());
    }

    if (params.offset) {
      searchParams.append("offset", params.offset.toString());
    }

    if (params.sort_by) {
      searchParams.append("sort_by", params.sort_by);
    }

    if (params.sort_dir) {
      searchParams.append("sort_dir", params.sort_dir);
    }

    const url = `/v1/objectives?${searchParams.toString()}`;

    return this._client.request<Pagination<Objective>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async update(
    projectId: string,
    objectiveId: string,
    params: ObjectiveUpdateParams,
  ): Promise<Objective> {
    const searchParams = new URLSearchParams({
      project_id: projectId,
    });

    const url = `/v1/objectives/${objectiveId}?${searchParams.toString()}`;

    return this._client.request<Objective>(url, {
      method: "PATCH",
      body: params,
      auth: true,
    });
  }
}
