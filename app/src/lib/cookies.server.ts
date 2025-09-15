import { cookies } from "next/headers";

export async function getProjectId(): Promise<string | null> {
  const cookieStore = await cookies();
  const projectId = cookieStore.get("project_id")?.value;

  return projectId ?? null;
}

export async function removeProjectId(): Promise<void> {
  const cookieStore = await cookies();
  cookieStore.delete("project_id");
}
