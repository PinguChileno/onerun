import { Agents } from "./resources/agents";
import { Objectives } from "./resources/objectives";
import { Projects } from "./resources/projects";
import { Simulations } from "./resources/simulations";

export class ApiError extends Error {
  constructor(
    public code: string,
    public message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class Client {
  private baseUrl: string;
  private token: string | null = null;
  private tokenPromise: Promise<string> | null = null;

  public agents: Agents;
  public objectives: Objectives;
  public projects: Projects;
  public simulations: Simulations;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.agents = new Agents(this);
    this.objectives = new Objectives(this);
    this.projects = new Projects(this);
    this.simulations = new Simulations(this);
  }

  setBaseUrl(url: string) {
    this.baseUrl = url;
  }

  setToken(token: string) {
    this.token = token;
  }

  clearToken() {
    this.token = null;
    this.tokenPromise = null;
  }

  private async getToken(): Promise<string> {
    if (this.token) {
      return this.token;
    }

    if (this.tokenPromise) {
      return this.tokenPromise;
    }

    this.tokenPromise = this.fetchToken();

    try {
      const token = await this.tokenPromise;
      this.token = token;
      return token;
    } finally {
      this.tokenPromise = null;
    }
  }

  private async fetchToken(): Promise<string> {
    if (typeof window !== "undefined") {
      const res = await fetch("/api/auth/token", {
        credentials: "include",
      });

      if (!res.ok) {
        throw new ApiError("AUTH_FAILED", "Failed to get authentication token");
      }

      const data = await res.json();
      return data.token;
    } else {
      throw new ApiError(
        "AUTH_REQUIRED",
        "Token must be provided in server environment",
      );
    }
  }

  async request<T = unknown>(
    endpoint: string,
    options: {
      method?: string;
      headers?: HeadersInit;
      body?: string | Record<string, unknown>;
      auth?: boolean;
    } = {},
  ): Promise<T> {
    const url = new URL(endpoint, this.baseUrl);

    const headers = new Headers(options.headers);

    if (options.auth !== false) {
      try {
        const token = await this.getToken();
        headers.set("Authorization", `Bearer ${token}`);
      } catch (error) {
        if (error instanceof ApiError && error.code === "AUTH_FAILED") {
          this.clearToken();
        }

        throw error;
      }
    }

    let body: string | undefined;

    if (options.body) {
      body =
        typeof options.body === "string"
          ? options.body
          : JSON.stringify(options.body);

      if (body) {
        headers.set("Content-Type", "application/json");
      }
    }

    const res = await fetch(url.toString(), {
      method: options.method,
      headers,
      body,
      credentials: typeof window !== "undefined" ? "include" : undefined,
    });

    if (!res.ok) {
      let error = {
        code: "UNKNOWN",
        message: "An unknown error occurred",
      };

      try {
        const result = await res.json();
        error = new ApiError(
          result.code ?? "UNKNOWN",
          result.message ?? result.detail,
        );
      } catch {}

      // Clear token on 401 to force refresh on next request
      if (res.status === 401) {
        this.clearToken();
      }

      throw error;
    }

    if (res.headers.get("Content-Type")?.includes("application/json")) {
      return res.json();
    }

    if (res.headers.get("Content-Type")?.includes("text/plain")) {
      return res.text() as T;
    }

    return undefined as unknown as T;
  }
}

export const client = new Client(
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:3001",
);
