import Cookies from "js-cookie";

export function getProjectId(): string | null {
  return Cookies.get("project_id") || null;
}

export function setProjectId(projectId: string): void {
  Cookies.set("project_id", projectId);
}

export function removeProjectId(): void {
  Cookies.remove("project_id");
}
