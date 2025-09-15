"use client";

import type * as React from "react";
import { DialogDescription } from "@radix-ui/react-dialog";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { Persona } from "@/lib/api/resources/simulations/personas";

import { ApprovalStatusBadge } from "./approval-status-badge";

export interface PersonaModalProps {
  isOpen: boolean;
  onClose: () => void;
  persona: Persona;
  targetPersonas: number;
}

export function PersonaModal({
  isOpen,
  onClose,
  persona,
  targetPersonas,
}: PersonaModalProps): React.JSX.Element {
  const attributes = persona.attributes;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="sm:max-w-4xl w-full flex flex-col gap-6 overflow-hidden"
        style={{
          maxHeight: "calc(100% - 48px)",
          height: "900px",
        }}
      >
        <DialogHeader>
          <DialogTitle className="text-2xl">
            {persona.summary} {persona.seq_id} / {targetPersonas}
          </DialogTitle>
          <DialogDescription className="hidden">
            View the details of this persona
          </DialogDescription>
        </DialogHeader>
        <div>
          <ApprovalStatusBadge status={persona.approval_status} />
        </div>
        <Tabs defaultValue="overview" className="flex flex-col gap-6 min-h-0">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="attributes">Attributes</TabsTrigger>
          </TabsList>
          <TabsContent value="overview" className="flex flex-col gap-4 min-h-0">
            <ScrollArea className="overflow-y-auto">
              <div className="flex flex-col gap-6 pr-4">
                {persona.story && (
                  <div className="flex flex-col gap-2">
                    <div className="text-sm font-medium text-muted-foreground">
                      Story
                    </div>
                    <div className="text-sm leading-relaxed">
                      {persona.story}
                    </div>
                  </div>
                )}
                {persona.purpose && (
                  <div className="flex flex-col gap-2">
                    <div className="text-sm font-medium text-muted-foreground">
                      Purpose
                    </div>
                    <div className="text-sm leading-relaxed">
                      {persona.purpose}
                    </div>
                  </div>
                )}
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent
            value="attributes"
            className="flex flex-col gap-4 min-h-0"
          >
            <ScrollArea className="overflow-y-auto">
              {attributes && Object.keys(attributes).length > 0 ? (
                <div className="grid grid-cols-1 gap-4">
                  {Object.entries(attributes)
                    .filter(([, value]) => value && value !== "")
                    .map(([key, value]) => (
                      <div
                        key={key}
                        className="space-y-2 p-4 border border-border/50 rounded-lg"
                      >
                        <div className="text-sm font-medium text-muted-foreground capitalize">
                          {key.replace(/_/g, " ")}
                        </div>
                        <div className="text-sm leading-relaxed">
                          {String(value)}
                        </div>
                      </div>
                    ))}
                </div>
              ) : (
                <div className="text-sm text-muted-foreground text-center py-8">
                  No attributes specified
                </div>
              )}
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
