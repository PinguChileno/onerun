import { APIResource } from "../resource";
import type { Pagination } from "../types";

export type Project = {
  id: string;
  name: string;
  created_at: string;
  updated_at: string;
};

export type ProjectCreateParams = {
  name: string;
};

export type ProjectUpdateParams = {
  name?: string | null;
};

export type ProjectListParams = {
  limit?: number;
  offset?: number;
  sort_by?: "created_at";
  sort_dir?: "asc" | "desc";
};

export class Projects extends APIResource {
  async create(params: ProjectCreateParams): Promise<Project> {
    const url = `/v1/projects`;

    return this._client.request<Project>(url, {
      method: "POST",
      body: params,
      auth: true,
    });
  }

  async list(params: ProjectListParams): Promise<Pagination<Project>> {
    const searchParams = new URLSearchParams({});

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

    const url = `/v1/projects?${searchParams.toString()}`;

    return this._client.request<Pagination<Project>>(url, {
      method: "GET",
      auth: true,
    });
  }

  async get(projectId: string): Promise<Project> {
    const url = `/v1/projects/${projectId}`;

    return this._client.request<Project>(url, {
      method: "GET",
      auth: true,
    });
  }

  async update(
    projectId: string,
    params: ProjectUpdateParams,
  ): Promise<Project> {
    const url = `/v1/projects/${projectId}`;

    return this._client.request<Project>(url, {
      method: "PATCH",
      body: params,
      auth: true,
    });
  }
}
