"use client";

import type * as React from "react";
import { SearchIcon, SortAscIcon, SortDescIcon } from "lucide-react";

import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAgentFiltersStore } from "@/stores/agent-filters-store";

export function AgentFilters(): React.JSX.Element {
  const { filters, setName, setSortBy, setSortDir } = useAgentFiltersStore();

  return (
    <div className="flex flex-col sm:flex-row gap-4 rounded-lg justify-between">
      <div className="flex-1 relative max-w-lg">
        <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search agents..."
          value={filters.name}
          onChange={(e) => setName(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="flex items-center gap-4">
        <Select
          value={`${filters.sortBy}-${filters.sortDir}`}
          onValueChange={(value) => {
            const [sortBy, sortDir] = value.split("-") as [
              typeof filters.sortBy,
              typeof filters.sortDir,
            ];
            setSortBy(sortBy);
            setSortDir(sortDir);
          }}
        >
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="name-asc">
              <div className="flex items-center gap-2">
                <SortAscIcon className="h-4 w-4" />
                Name A-Z
              </div>
            </SelectItem>
            <SelectItem value="name-desc">
              <div className="flex items-center gap-2">
                <SortDescIcon className="h-4 w-4" />
                Name Z-A
              </div>
            </SelectItem>
            <SelectItem value="created_at-desc">
              <div className="flex items-center gap-2">
                <SortDescIcon className="h-4 w-4" />
                Newest First
              </div>
            </SelectItem>
            <SelectItem value="created_at-asc">
              <div className="flex items-center gap-2">
                <SortAscIcon className="h-4 w-4" />
                Oldest First
              </div>
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
