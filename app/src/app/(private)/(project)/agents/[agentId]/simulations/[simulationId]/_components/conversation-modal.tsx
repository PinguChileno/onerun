"use client";

import * as React from "react";
import { Waveform } from "ldrs/react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useListConversationItemsQuery } from "@/data/get-conversation-items-query";
import { useGetConversationQuery } from "@/data/get-conversation-query";
import type {
  ConversationEvaluation,
  ConversationItem,
} from "@/lib/api/resources/simulations/conversations";
import { cn } from "@/lib/utils";

import { ConversationStatusBadge } from "./conversation-status-badge";
import { EvaluationStatusBadge } from "./evaluation-status-badge";

function renderAverageScore(
  evaluations: ConversationEvaluation[],
): React.JSX.Element {
  if (evaluations.length === 0) {
    return (
      <div className="flex items-center gap-1 font-mono text-sm">
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
    <div className="flex items-center gap-1 font-mono text-sm">
      <span className="font-medium text-foreground">{value}</span>
      <span className="text-muted-foreground">/</span>
      <span className="text-muted-foreground">10</span>
    </div>
  );
}

export interface ConversationModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectId: string;
  simulationId: string;
  conversationId: string;
  targetConversations: number;
}

export function ConversationModal({
  isOpen,
  onClose,
  projectId,
  simulationId,
  conversationId,
  targetConversations,
}: ConversationModalProps): React.JSX.Element {
  const {
    data: conversation,
    error,
    isLoading,
  } = useGetConversationQuery(projectId, simulationId, conversationId);

  const renderContent = (): React.JSX.Element | null => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    if (!conversation) {
      return null;
    }

    return (
      <div className="flex flex-col gap-6 min-h-0">
        <div className="flex flex-col gap-4">
          <div className="grid grid-cols-3 gap-4 border-b border-t py-4">
            <div className="flex flex-col items-center gap-2">
              <span className="text-sm text-muted-foreground">Status</span>
              <ConversationStatusBadge status={conversation.status} />
            </div>
            <div className="flex flex-col items-center gap-2">
              <span className="text-sm text-muted-foreground">Evaluation</span>
              <EvaluationStatusBadge status={conversation.evaluation_status} />
            </div>
            <div className="flex flex-col items-center gap-2">
              <span className="text-sm text-muted-foreground">Score</span>
              {renderAverageScore(conversation.evaluations ?? [])}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 min-w-0">
          <span className="text-sm text-muted-foreground">Persona</span>
          <span className="text-sm font-medium truncate max-w-xs">
            {conversation.persona?.summary || "Unknown"}
          </span>
        </div>
        <Tabs defaultValue="messages" className="flex flex-col gap-6 min-h-0">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="messages">Messages</TabsTrigger>
            <TabsTrigger value="evaluations">Evaluations</TabsTrigger>
          </TabsList>
          <TabsContent value="messages" className="flex flex-col gap-4 min-h-0">
            <Messages
              conversationId={conversationId}
              projectId={projectId}
              simulationId={simulationId}
            />
          </TabsContent>
          <TabsContent
            value="evaluations"
            className="flex flex-col gap-4 min-h-0"
          >
            <Evaluations evaluations={conversation.evaluations ?? []} />
          </TabsContent>
        </Tabs>
      </div>
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="sm:max-w-3xl w-full flex flex-col gap-6 overflow-hidden"
        style={{
          maxHeight: "calc(100% - 48px)",
          height: "800px",
        }}
      >
        <DialogHeader>
          <DialogTitle className="text-xl">
            Conversation{" "}
            {conversation
              ? `${conversation.seq_id}/${targetConversations}`
              : ""}
          </DialogTitle>
          <DialogDescription className="hidden">
            View the details of this conversation
          </DialogDescription>
        </DialogHeader>
        {renderContent()}
      </DialogContent>
    </Dialog>
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

interface MessagesProps {
  conversationId: string;
  projectId: string;
  simulationId: string;
}

function Messages({ conversationId, projectId, simulationId }: MessagesProps) {
  const { data, error, isLoading } = useListConversationItemsQuery(
    projectId,
    simulationId,
    conversationId,
  );

  const renderContent = (): React.JSX.Element => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    const items = data?.data ?? [];

    if (items.length === 0) {
      return (
        <div className="py-8 text-center text-muted-foreground">
          No messages available.
        </div>
      );
    }

    return (
      <ScrollArea className="flex flex-col overflow-y-auto">
        <div className="flex flex-col gap-8 pr-4">
          {items.map((item) => (
            <Message key={item.id} item={item} />
          ))}
        </div>
      </ScrollArea>
    );
  };

  return renderContent();
}

interface MessageProps {
  item: ConversationItem;
}

function Message({ item }: MessageProps): React.JSX.Element {
  return (
    <div className="flex flex-col">
      <div
        className={cn(
          "flex flex-col gap-2 max-w-[70%] group",
          item.role === "user" ? "self-end" : "",
        )}
      >
        <div className={cn("p-3 rounded-lg bg-muted ")}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-muted-foreground">
              {item.role === "user" ? "Persona" : "Agent"}
            </span>
          </div>
          <div className="text-sm">
            {item.content.map((content, index) => (
              // biome-ignore lint/suspicious/noArrayIndexKey: allow
              <div key={index}>{content.text}</div>
            ))}
          </div>
        </div>
        <span className="text-xs text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          {new Date(item.created_at).toLocaleString()}
        </span>
      </div>
    </div>
  );
}

interface EvaluationsProps {
  evaluations: ConversationEvaluation[];
}

function Evaluations({ evaluations }: EvaluationsProps): React.JSX.Element {
  if (evaluations.length === 0) {
    return (
      <div className="py-8 text-center text-muted-foreground">
        No evaluations available.
      </div>
    );
  }

  return (
    <ScrollArea className="flex flex-col overflow-y-auto">
      <div className="flex flex-col gap-4 pr-4">
        {evaluations.map((score) => (
          <Evaluation key={score.id} evaluation={score} />
        ))}
      </div>
    </ScrollArea>
  );
}

interface EvaluationProps {
  evaluation: ConversationEvaluation;
}

function Evaluation({ evaluation }: EvaluationProps): React.JSX.Element {
  const [isExpanded, setIsExpanded] = React.useState<boolean>(false);
  const value = Math.round(evaluation.score * 100) / 10; // Convert to 0-10 scale and round to 1 decimal

  const shouldShowToggle = evaluation.reason.length > 100;
  const displayReason =
    isExpanded || !shouldShowToggle
      ? evaluation.reason
      : `${evaluation.reason.slice(0, 100)}...`;

  return (
    <Card>
      <CardContent className="p-4 flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="font-semibold">{evaluation.objective?.name}</div>
          <div className="flex items-center gap-1 font-mono text-sm">
            <span className="font-medium text-foreground">{value}</span>
            <span className="text-muted-foreground">/</span>
            <span className="text-muted-foreground">10</span>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="text-sm text-muted-foreground">{displayReason}</div>
          {shouldShowToggle && (
            <Button
              variant="ghost"
              size="sm"
              className="cursor-pointer"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              {isExpanded ? "Show Less" : "Show More"}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
