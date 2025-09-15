"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import {
  ArrowRightIcon,
  ExternalLinkIcon,
  Loader2Icon,
  XIcon,
} from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { useCreateSimulationMutation } from "@/data/create-simulation-mutation";
import { useListObjectivesQuery } from "@/data/list-objectives-query";
import { queryKeys } from "@/data/query-keys";
import { ApiError } from "@/lib/api/client";

const createSchema = z.object({
  auto_approve: z.boolean(),
  name: z.string().min(1, "Name is required"),
  objective_ids: z.array(z.string()).optional(),
  scenario: z.string().min(1, "Scenario is required"),
  target_conversations: z
    .number()
    .min(1, "Must be at least 1")
    .max(2000, "Cannot be more than 2000"),
  target_personas: z
    .number()
    .min(1, "Must be at least 1")
    .max(2000, "Cannot be more than 100"),
  max_turns: z
    .number()
    .min(1, "Must be at least 1")
    .max(25, "Cannot be more than 25"),
});

type CreateSchema = z.infer<typeof createSchema>;

interface CreateSimulationDrawerProps {
  isOpen: boolean;
  onClose?: () => void;
  agentId: string;
  projectId: string;
}

export function CreateSimulationDrawer({
  isOpen,
  onClose,
  agentId,
  projectId,
}: CreateSimulationDrawerProps): React.JSX.Element {
  const queryClient = useQueryClient();
  const createMutation = useCreateSimulationMutation();
  const { data: objectivesData } = useListObjectivesQuery(projectId, {});

  const form = useForm<CreateSchema>({
    resolver: zodResolver(createSchema),
    defaultValues: {
      name: "",
      scenario: "",
      target_personas: 5,
      target_conversations: 10,
      max_turns: 5,
      auto_approve: false,
      objective_ids: [],
    },
  });

  const onSubmit = async (data: CreateSchema) => {
    try {
      await createMutation.mutateAsync({
        projectId,
        params: {
          ...data,
          agent_id: agentId,
        },
      });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    onClose?.();
    form.reset();
    toast.success("Simulation created successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.simulations.all(projectId),
    });
  };

  React.useEffect(() => {
    if (!isOpen) {
      form.reset();
    }
  }, [isOpen, form]);

  const objectives = objectivesData?.data ?? [];
  const objectivesCount = objectives.length;
  const selectedObjectives = form.watch("objective_ids") ?? [];
  const selectedObjectivesCount = selectedObjectives.length;

  return (
    <Drawer open={isOpen} onOpenChange={onClose} direction="right">
      <DrawerContent className="h-full w-full" style={{ maxWidth: "512px" }}>
        <DrawerHeader>
          <DrawerTitle>Simulation Configuration</DrawerTitle>
          <DrawerDescription className="hidden">
            Define the parameters for your new simulation.
          </DrawerDescription>
          <DrawerClose asChild>
            <Button
              variant="ghost"
              size="sm"
              className="absolute right-4 top-4 text-muted-foreground"
            >
              <XIcon />
            </Button>
          </DrawerClose>
        </DrawerHeader>
        <ScrollArea className="flex flex-col overflow-y-auto">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex-1 flex flex-col gap-6 p-6"
            >
              <div className="flex flex-col gap-4">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Name</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="E.g., Policy Compliance Test"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="scenario"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Scenario</FormLabel>
                      <FormControl>
                        <Textarea
                          {...field}
                          className="min-h-20"
                          placeholder="E.g., Simulate a user trying to access restricted content without proper authorization."
                          rows={4}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <Separator />
              <div className="flex flex-col gap-4">
                <FormField
                  control={form.control}
                  name="target_personas"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Number of Personas</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          min="1"
                          max="100"
                          {...field}
                          onChange={(e) =>
                            field.onChange(Number(e.target.value))
                          }
                        />
                      </FormControl>
                      <FormDescription>
                        Personas simulate different user behaviours (1-100)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="target_conversations"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Target Conversations</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          min="1"
                          max="2000"
                          {...field}
                          onChange={(e) =>
                            field.onChange(Number(e.target.value))
                          }
                        />
                      </FormControl>
                      <FormDescription>
                        Maximum total number of conversations (1-2000)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="max_turns"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Max Turns</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          min="1"
                          max="25"
                          {...field}
                          onChange={(e) =>
                            field.onChange(Number(e.target.value))
                          }
                        />
                      </FormControl>
                      <FormDescription>
                        Maximum messages exchanged between agent and persona
                        (1-25)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="auto_approve"
                  render={({ field }) => (
                    <FormItem className="flex items-center space-x-2">
                      <FormControl>
                        <Checkbox
                          checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                      </FormControl>
                      <FormLabel className="text-sm font-medium">
                        Auto-approve generated personas
                      </FormLabel>
                    </FormItem>
                  )}
                />
              </div>
              <Separator />
              <FormField
                control={form.control}
                name="objective_ids"
                render={({ field }) => (
                  <FormItem>
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex flex-col gap-2">
                        <FormLabel>Objectives</FormLabel>
                        <FormDescription>
                          Select the objectives you want to test your LLM
                          against
                        </FormDescription>
                      </div>
                      <Button variant="secondary" size="sm" asChild>
                        <a target="_blank" rel="noreferrer" href="/objectives">
                          Create Objective
                          <ExternalLinkIcon />
                        </a>
                      </Button>
                    </div>
                    <FormControl>
                      <ScrollArea className="max-h-40 border rounded-md">
                        <div className="flex flex-col gap-2 min-h-20 p-3">
                          {objectives.map((objective) => (
                            <div
                              key={objective.id}
                              className="flex items-center gap-2"
                            >
                              <Checkbox
                                id={`objective-${objective.id}`}
                                checked={
                                  field.value?.includes(objective.id) || false
                                }
                                onCheckedChange={(checked) => {
                                  const currentIds = field.value || [];
                                  if (checked) {
                                    field.onChange([
                                      ...currentIds,
                                      objective.id,
                                    ]);
                                  } else {
                                    field.onChange(
                                      currentIds.filter(
                                        (id) => id !== objective.id,
                                      ),
                                    );
                                  }
                                }}
                              />
                              <Label
                                htmlFor={`objective-${objective.id}`}
                                className="text-sm font-normal cursor-pointer flex-1"
                              >
                                {objective.name}
                              </Label>
                            </div>
                          ))}
                          {!objectivesCount ? (
                            <div className="text-sm text-muted-foreground">
                              No objectives available
                            </div>
                          ) : null}
                        </div>
                      </ScrollArea>
                    </FormControl>
                    <FormDescription>
                      {selectedObjectivesCount} of {objectivesCount} objectives
                      selected
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div>
                <Button
                  type="submit"
                  disabled={createMutation.isPending}
                  className="w-full"
                >
                  {createMutation.isPending ? (
                    <Loader2Icon className="animate-spin" />
                  ) : null}
                  Create
                  <ArrowRightIcon />
                </Button>
              </div>
            </form>
          </Form>
        </ScrollArea>
      </DrawerContent>
    </Drawer>
  );
}
