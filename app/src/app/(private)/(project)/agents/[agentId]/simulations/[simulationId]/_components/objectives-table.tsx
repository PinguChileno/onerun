import type * as React from "react";

import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Objective } from "@/lib/api/resources/objectives";

export interface ObjectivesTableProps {
  objectives: Objective[];
}

export function ObjectivesTable({
  objectives,
}: ObjectivesTableProps): React.JSX.Element {
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
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}

function Empty(): React.JSX.Element {
  return (
    <Card>
      <CardContent className="py-12">
        <div className="text-center text-muted-foreground">
          No objectives assigned
        </div>
      </CardContent>
    </Card>
  );
}
