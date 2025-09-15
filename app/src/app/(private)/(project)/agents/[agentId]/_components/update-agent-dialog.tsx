"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { Loader2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { queryKeys } from "@/data/query-keys";
import { useUpdateAgentMutation } from "@/data/update-agent-mutation";
import { ApiError } from "@/lib/api/client";
import type { Agent } from "@/lib/api/resources/agents";

const updateSchema = z.object({
  description: z.string().max(2000),
  name: z.string().min(1, "Name is required"),
});

type UpdateSchema = z.infer<typeof updateSchema>;

export interface UpdateAgentDialogProps {
  agent: Agent;
  projectId: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function UpdateAgentDialog({
  agent,
  projectId,
  open,
  onOpenChange,
}: UpdateAgentDialogProps) {
  const updateMutation = useUpdateAgentMutation();
  const queryClient = useQueryClient();

  const form = useForm<UpdateSchema>({
    resolver: zodResolver(updateSchema),
    defaultValues: {
      name: agent.name,
      description: agent.description || "",
    },
  });

  React.useEffect(() => {
    if (open) {
      form.reset({
        name: agent.name,
        description: agent.description || "",
      });
    }
  }, [open, agent, form]);

  const onSubmit = async (data: UpdateSchema): Promise<void> => {
    try {
      await updateMutation.mutateAsync({
        projectId,
        agentId: agent.id,
        params: data,
      });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    onOpenChange(false);
    toast.success("Agent updated successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.agents.get(projectId, agent.id),
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md sm:w-full gap-0 p-0">
        <DialogHeader className="py-5 px-5">
          <DialogTitle>Update Agent</DialogTitle>
          <DialogDescription className="hidden">
            Update agent details
          </DialogDescription>
        </DialogHeader>
        <div className="px-5 pb-5">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex flex-col gap-4"
            >
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Agent Name</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder="Enter agent name"
                        autoComplete="agentName"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Agent Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Enter agent summary and capabilities"
                        className="min-h-[100px]"
                        autoComplete="off"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="flex gap-2 justify-end">
                <Button type="submit" disabled={updateMutation.isPending}>
                  {updateMutation.isPending ? (
                    <Loader2Icon className="animate-spin" />
                  ) : null}
                  Save Changes
                </Button>
              </div>
            </form>
          </Form>
        </div>
      </DialogContent>
    </Dialog>
  );
}
