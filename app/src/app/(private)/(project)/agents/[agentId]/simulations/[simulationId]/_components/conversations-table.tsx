"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";

import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useListConversationsQuery } from "@/data/list-conversations-query";
import type { ConversationEvaluation } from "@/lib/api/resources/simulations/conversations";

import { ConversationModal } from "./conversation-modal";
import { ConversationStatusBadge } from "./conversation-status-badge";
import { EvaluationStatusBadge } from "./evaluation-status-badge";

function renderAverageScore(
  evaluations: ConversationEvaluation[] | null,
): React.JSX.Element {
  if (!evaluations || evaluations.length === 0) {
    return (
      <div className="font-mono text-sm">
        <span className="text-muted-foreground">-</span>
      </div>
    );
  }

  const sum = evaluations.reduce(
    (acc, evaluation) => acc + evaluation.score,
    0,
  );
  const avg = sum / evaluations.length;
  const value = Math.round(avg * 100) / 10; // Convert to 0-10 scale and round to 1 decimal

  return (
    <div className="font-mono text-sm">
      <span className="font-medium text-foreground">{value}</span>
      <span className="text-muted-foreground">/</span>
      <span className="text-muted-foreground">10</span>
    </div>
  );
}

interface ConversationsTableProps {
  simulationId: string;
  projectId: string;
  targetConversations: number;
}

export function ConversationsTable({
  simulationId,
  projectId,
  targetConversations,
}: ConversationsTableProps): React.JSX.Element {
  const [selectedConversationId, setSelectedConversationId] = React.useState<
    string | null
  >(null);

  const { data, error, isLoading } = useListConversationsQuery(
    projectId,
    simulationId,
    {},
  );

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const conversations = data?.data ?? [];

    if (conversations.length === 0) {
      return <Empty />;
    }

    return (
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">ID</TableHead>
              <TableHead>Persona</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>End Reason</TableHead>
              <TableHead>Evaluation</TableHead>
              <TableHead className="text-right">Average Score</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {conversations.map((conversation) => (
              <TableRow
                key={conversation.id}
                className="cursor-pointer hover:bg-muted/50"
                onClick={() => setSelectedConversationId(conversation.id)}
              >
                <TableCell className="w-[80px]">
                  <span className="font-medium">{conversation.seq_id}</span>
                </TableCell>
                <TableCell>
                  <span className="font-medium">
                    {conversation.persona
                      ? conversation.persona.summary
                      : "N/A"}
                  </span>
                </TableCell>
                <TableCell>
                  <ConversationStatusBadge status={conversation.status} />
                </TableCell>
                <TableCell>
                  <span className="text-muted-foreground">
                    {conversation.end_reason || "-"}
                  </span>
                </TableCell>
                <TableCell>
                  <EvaluationStatusBadge
                    status={conversation.evaluation_status}
                  />
                </TableCell>
                <TableCell className="text-right">
                  {renderAverageScore(conversation.evaluations)}
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
      {selectedConversationId && (
        <ConversationModal
          isOpen={!!selectedConversationId}
          onClose={() => setSelectedConversationId(null)}
          projectId={projectId}
          simulationId={simulationId}
          conversationId={selectedConversationId}
          targetConversations={targetConversations}
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
          No conversations yet
        </div>
      </CardContent>
    </Card>
  );
}
