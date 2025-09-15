import { create } from "zustand";

import type { Project } from "@/lib/api/resources/projects";

export interface CurrentProjectState {
  currentProject: Project | null;
  setCurrentProject: (project: Project | null) => void;
}

export const useCurrentProjectStore = create<CurrentProjectState>()((set) => ({
  currentProject: null,
  setCurrentProject: (project) => set({ currentProject: project }),
}));
