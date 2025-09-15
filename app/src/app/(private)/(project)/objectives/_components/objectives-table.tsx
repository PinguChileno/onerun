"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";
import { EditIcon } from "lucide-react";

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
import { useListObjectivesQuery } from "@/data/list-objectives-query";
import type { Objective } from "@/lib/api/resources/objectives";

import { UpdateObjectiveDialog } from "./update-objective-dialog";

export interface ObjectivesTableProps {
  projectId: string;
}

export function ObjectivesTable({
  projectId,
}: ObjectivesTableProps): React.JSX.Element {
  const { data, error, isLoading } = useListObjectivesQuery(projectId, {});
  const [selectedObjective, setSelectedObjective] =
    React.useState<Objective | null>(null);

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const objectives = data?.data ?? [];

    if (objectives.length === 0) {
      return <Empty />;
    }

    return (
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="max-w-sm">Name</TableHead>
              <TableHead className="max-w-sm">Criteria</TableHead>
              <TableHead className="w-24 text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {objectives.map((objective) => (
              <TableRow key={objective.id}>
                <TableCell className="max-w-sm font-semibold">
                  {objective.name}
                </TableCell>
                <TableCell className="max-w-sm truncate text-muted-foreground">
                  {objective.criteria}
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedObjective(objective)}
                  >
                    <EditIcon />
                  </Button>
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
      <UpdateObjectiveDialog
        objective={selectedObjective}
        projectId={projectId}
        onClose={() => setSelectedObjective(null)}
      />
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
          No objectives yet
        </div>
      </CardContent>
    </Card>
  );
}
