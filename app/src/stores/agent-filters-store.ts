import { create } from "zustand";
import { devtools } from "zustand/middleware";

export interface AgentFilters {
  name: string;
  sortBy: "created_at" | "updated_at";
  sortDir: "asc" | "desc";
}

interface AgentFiltersState {
  filters: AgentFilters;
  setName: (name: string) => void;
  setSortBy: (sortBy: AgentFilters["sortBy"]) => void;
  setSortDir: (sortOrder: AgentFilters["sortDir"]) => void;
  setFilters: (filters: Partial<AgentFilters>) => void;
  resetFilters: () => void;
}

const defaultFilters: AgentFilters = {
  name: "",
  sortBy: "created_at",
  sortDir: "asc",
};

export const useAgentFiltersStore = create<AgentFiltersState>()(
  devtools(
    (set) => ({
      filters: defaultFilters,

      setName: (name: string) => {
        return set(
          (state) => ({
            filters: { ...state.filters, name },
          }),
          false,
          "setName",
        );
      },

      setSortBy: (sortBy: AgentFilters["sortBy"]) => {
        return set(
          (state) => ({
            filters: { ...state.filters, sortBy },
          }),
          false,
          "setSortBy",
        );
      },

      setSortDir: (sortOrder: AgentFilters["sortDir"]) => {
        return set(
          (state) => ({
            filters: { ...state.filters, sortDir: sortOrder },
          }),
          false,
          "setSortOrder",
        );
      },

      setFilters: (newFilters: Partial<AgentFilters>) => {
        return set(
          (state) => ({
            filters: { ...state.filters, ...newFilters },
          }),
          false,
          "setFilters",
        );
      },

      resetFilters: () => {
        return set({ filters: defaultFilters }, false, "resetFilters");
      },
    }),
    {
      name: "agent-filters",
    },
  ),
);
