"use client";

import * as React from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Waveform } from "ldrs/react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useApprovePersonaMutation } from "@/data/approve-persona-mutation";
import { useListPersonasQuery } from "@/data/list-personas-query";
import { queryKeys } from "@/data/query-keys";
import { useRejectPersonaMutation } from "@/data/reject-persona-mutation";
import { ApiError } from "@/lib/api/client";
import type { Persona } from "@/lib/api/resources/simulations/personas";

import { ApprovalStatusBadge } from "./approval-status-badge";
import { PersonaModal } from "./persona-modal";

export interface PersonasTableProps {
  projectId: string;
  simulationId: string;
  targetPersonas: number;
}

export function PersonasTable({
  projectId,
  simulationId,
  targetPersonas,
}: PersonasTableProps): React.JSX.Element {
  const queryClient = useQueryClient();

  const [selectedPersona, setSelectedPersona] = React.useState<Persona | null>(
    null,
  );

  const { data, error, isLoading } = useListPersonasQuery(
    projectId,
    simulationId,
  );

  const approveMutation = useApprovePersonaMutation();
  const rejectMutation = useRejectPersonaMutation();

  const handleApprove = async (personaId: string): Promise<void> => {
    try {
      await approveMutation.mutateAsync({
        projectId: projectId,
        simulationId: simulationId,
        personaId: personaId,
      });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    toast.success("Persona approved");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.simulations.all(projectId),
    });
  };

  const handleReject = async (personaId: string): Promise<void> => {
    try {
      await rejectMutation.mutateAsync({
        projectId: projectId,
        simulationId: simulationId,
        personaId: personaId,
      });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    toast.success("Persona rejected");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.simulations.all(projectId),
    });
  };

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const personas = data?.data ?? [];

    if (personas.length === 0) {
      return <Empty />;
    }

    return (
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">ID</TableHead>
              <TableHead>Summary</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {personas.map((persona) => (
              <TableRow key={persona.id} className="hover:bg-muted/20">
                <TableCell className="w-[80px]">
                  <span className="font-medium">{persona.seq_id} </span>
                </TableCell>
                <TableCell>
                  <button
                    className="font-medium cursor-pointer hover:underline"
                    onClick={() => {
                      setSelectedPersona(persona);
                    }}
                    type="button"
                  >
                    {persona.summary}
                  </button>
                </TableCell>
                <TableCell>
                  <ApprovalStatusBadge status={persona.approval_status} />
                </TableCell>
                <TableCell className="text-right">
                  {persona.approval_status === "pending" ? (
                    <div className="flex justify-end gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleReject(persona.id);
                        }}
                        disabled={rejectMutation.isPending}
                      >
                        Reject
                      </Button>
                      <Button
                        size="sm"
                        className="cursor-pointer"
                        variant="outline"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleApprove(persona.id);
                        }}
                        disabled={approveMutation.isPending}
                      >
                        Approve
                      </Button>
                    </div>
                  ) : null}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    );
  };

  return (
    <>
      {renderContent()}
      {selectedPersona ? (
        <PersonaModal
          isOpen={!!selectedPersona}
          onClose={() => setSelectedPersona(null)}
          persona={selectedPersona}
          targetPersonas={targetPersonas}
        />
      ) : null}
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
    <div className="py-12">
      <p className="text-center text-muted-foreground">{message}</p>
    </div>
  );
}

function Empty(): React.JSX.Element {
  return (
    <Card>
      <CardContent className="py-12">
        <div className="text-center text-muted-foreground">
          No personas generated yet
        </div>
      </CardContent>
    </Card>
  );
}
