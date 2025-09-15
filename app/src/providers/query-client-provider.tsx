"use client";

import type * as React from "react";
import { QueryClientProvider } from "@tanstack/react-query";

import { queryClient } from "@/lib/query-client";

interface ProviderProps {
  children: React.ReactNode;
}

function QueryClientProviderWrapper({
  children,
}: ProviderProps): React.JSX.Element {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export { QueryClientProviderWrapper as QueryClientProvider };
