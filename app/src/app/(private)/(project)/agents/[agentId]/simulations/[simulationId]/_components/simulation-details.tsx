"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";
import { MessageSquareIcon, MoreVerticalIcon, UsersIcon } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useCancelSimulationMutation } from "@/data/cancel-simulation-mutation";
import { useGetSimulationQuery } from "@/data/get-simulation-query";
import { ApiError } from "@/lib/api/client";
import type { Agent } from "@/lib/api/resources/agents";

import { SimulationStatusBadge } from "../../../_components/simulation-status-badge";
import { ConversationsTable } from "./conversations-table";
import { ObjectivesTable } from "./objectives-table";
import { PersonasTable } from "./personas-table";

export interface SimulationDetailsProps {
  agentId: string;
  simulationId: string;
  projectId: string;
}

export function SimulationDetails({
  projectId,
  simulationId,
}: SimulationDetailsProps): React.JSX.Element {
  const [activeTab, setActiveTab] = React.useState<string>("objectives");

  const {
    data: simulation,
    error,
    isLoading,
  } = useGetSimulationQuery(projectId, simulationId);

  const cancelMutation = useCancelSimulationMutation();

  const handleCancel = async (): Promise<void> => {
    try {
      await cancelMutation.mutateAsync({ projectId, simulationId });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    toast.success("Simulation scheduled for cancellation");
  };

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    if (!simulation) {
      return <NotFound />;
    }

    const agent = simulation.agent as Agent;

    return (
      <div>
        <div className="flex flex-col gap-4 py-6 border-b">
          <div className="flex justify-between items-start">
            <div className="flex flex-col gap-4">
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
                  <BreadcrumbSeparator />
                  <BreadcrumbItem>{simulation.name}</BreadcrumbItem>
                </BreadcrumbList>
              </Breadcrumb>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-4">
                  <div className="text-2xl font-bold">{simulation.name}</div>
                  <SimulationStatusBadge status={simulation.status} />
                </div>
                {simulation.scenario ? (
                  <div className="text-muted-foreground">
                    {simulation.scenario}
                  </div>
                ) : null}
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
                    disabled={
                      !["in_progress", "pending", "queued"].includes(
                        simulation.status,
                      )
                    }
                    onSelect={handleCancel}
                    variant="destructive"
                  >
                    Cancel
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <UsersIcon className="h-4 w-4" />
                  Target Personas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">
                  {simulation.target_personas}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <MessageSquareIcon className="h-4 w-4" />
                  Target Conversations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">
                  {simulation.target_conversations}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  <MessageSquareIcon className="h-4 w-4" />
                  Max Turns
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">{simulation.max_turns}</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">
                  Auto-approve
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">
                  {simulation.auto_approve ? "Yes" : "No"}
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
        <Tabs
          value={activeTab}
          onValueChange={setActiveTab}
          className="flex flex-col gap-4 py-6"
        >
          <TabsList>
            <TabsTrigger value="objectives">Objectives</TabsTrigger>
            <TabsTrigger value="personas">Personas</TabsTrigger>
            <TabsTrigger value="conversations">Conversations</TabsTrigger>
          </TabsList>
          <TabsContent value="objectives">
            <ObjectivesTable objectives={simulation.objectives} />
          </TabsContent>
          <TabsContent value="personas">
            <PersonasTable
              simulationId={simulation.id}
              projectId={simulation.project_id}
              targetPersonas={simulation.target_personas}
            />
          </TabsContent>
          <TabsContent value="conversations">
            <ConversationsTable
              simulationId={simulation.id}
              projectId={simulation.project_id}
              targetConversations={simulation.target_conversations}
            />
          </TabsContent>
        </Tabs>
      </div>
    );
  };

  return renderContent();
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
      <p className="text-muted-foreground">Simulation not found</p>
    </div>
  );
}
