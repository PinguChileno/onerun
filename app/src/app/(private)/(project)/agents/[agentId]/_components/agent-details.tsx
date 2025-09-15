"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";
import { CheckCircleIcon, MoreVerticalIcon } from "lucide-react";
import Link from "next/link";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { useGetAgentQuery } from "@/data/get-agent-query";
import { useCopy } from "@/hooks/use-copy";

import { CreateSimulationDrawer } from "./create-simulation-drawer";
import { SimulationsSection } from "./simulations-section";
import { UpdateAgentDialog } from "./update-agent-dialog";

export interface AgentDetailsProps {
  agentId: string;
  projectId: string;
}

export function AgentDetails({
  agentId,
  projectId,
}: AgentDetailsProps): React.JSX.Element {
  const [isDrawerOpen, setIsDrawerOpen] = React.useState<boolean>(false);
  const [isUpdateDialogOpen, setIsUpdateDialogOpen] =
    React.useState<boolean>(false);

  const { copy, copied } = useCopy();

  const {
    data: agent,
    error,
    isLoading,
  } = useGetAgentQuery(projectId, agentId);

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    if (!agent) {
      return <NotFound />;
    }

    return (
      <div className="flex-1 flex flex-col">
        <div className="flex flex-col gap-4 py-6 border-b">
          <div className="flex justify-between items-start">
            <div className="flex flex-col gap-4 min-w-0 flex-1">
              <Breadcrumb>
                <BreadcrumbList>
                  <BreadcrumbItem>
                    <BreadcrumbLink asChild>
                      <Link href="/agents">Agents</Link>
                    </BreadcrumbLink>
                  </BreadcrumbItem>
                  <BreadcrumbSeparator />
                  <BreadcrumbItem>
                    <BreadcrumbLink asChild>
                      <Link href={`/agents/${agent.id}`}>{agent.name}</Link>
                    </BreadcrumbLink>
                  </BreadcrumbItem>
                </BreadcrumbList>
              </Breadcrumb>
              <div className="flex items-center gap-2 min-w-0">
                <Avatar className="bg-background-3 h-12 w-12">
                  <AvatarFallback className="bg-background-3 text-lg text-foreground font-medium uppercase">
                    {agent.name.slice(0, 2)}
                  </AvatarFallback>
                </Avatar>
                <div className="max-w-lg">
                  <div className="flex items-center gap-2">
                    <div className="text-2xl font-bold">{agent.name}</div>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <button
                          className="cursor-pointer rounded-full py-1 px-2 bg-background-2 text-sm text-muted-foreground hover:bg-background-3 flex items-center gap-1"
                          onClick={() => copy(agent.id)}
                          type="button"
                        >
                          ID: {agent.id}
                          {copied && <CheckCircleIcon className="h-3 w-3" />}
                        </button>
                      </TooltipTrigger>
                      <TooltipContent side="right">Copy</TooltipContent>
                    </Tooltip>
                  </div>
                  {agent.description ? (
                    <div className="truncate text-muted-foreground">
                      {agent.description}
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
            <div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    className="cursor-pointer"
                    size="icon"
                    variant="outline"
                  >
                    <MoreVerticalIcon />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onSelect={() => setIsUpdateDialogOpen(true)}
                  >
                    Edit
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
        <SimulationsSection
          agentId={agent.id}
          projectId={projectId}
          onCreate={() => setIsDrawerOpen(true)}
        />
      </div>
    );
  };

  return (
    <>
      {renderContent()}
      <CreateSimulationDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        agentId={agentId}
        projectId={projectId}
      />
      {agent && (
        <UpdateAgentDialog
          agent={agent}
          projectId={projectId}
          open={isUpdateDialogOpen}
          onOpenChange={setIsUpdateDialogOpen}
        />
      )}
    </>
  );
}

function Loading(): React.JSX.Element {
  return (
    <div className="flex justify-center py-12">
      <Waveform size="35" stroke="3.5" speed="1" color="white" />
    </div>
  );
}

interface ErrorDisplayProps {
  message: string;
}

function ErrorDisplay({ message }: ErrorDisplayProps): React.JSX.Element {
  return (
    <div className="text-center py-12">
      <p className="text-muted-foreground">{message}</p>
    </div>
  );
}

function NotFound(): React.JSX.Element {
  return (
    <div className="text-center py-12">
      <p className="text-muted-foreground">Agent not found</p>
    </div>
  );
}
