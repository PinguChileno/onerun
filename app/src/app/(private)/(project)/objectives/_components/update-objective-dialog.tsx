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
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
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
import { Textarea } from "@/components/ui/textarea";
import { queryKeys } from "@/data/query-keys";
import { useUpdateObjectiveMutation } from "@/data/update-objective-mutation";
import { ApiError } from "@/lib/api/client";
import type { Objective } from "@/lib/api/resources/objectives";

const updateSchema = z.object({
  name: z.string().min(1, "Name is required").optional().or(z.literal("")),
  criteria: z
    .string()
    .min(1, "Criteria is required")
    .optional()
    .or(z.literal("")),
});

type UpdateSchema = z.infer<typeof updateSchema>;

export interface UpdateObjectiveDialogProps {
  objective: Objective | null;
  projectId: string;
  onClose: () => void;
}

export function UpdateObjectiveDialog({
  objective,
  projectId,
  onClose,
}: UpdateObjectiveDialogProps) {
  const updateMutation = useUpdateObjectiveMutation();
  const queryClient = useQueryClient();

  const form = useForm<UpdateSchema>({
    resolver: zodResolver(updateSchema),
    defaultValues: {
      name: "",
      criteria: "",
    },
  });

  React.useEffect(() => {
    if (objective) {
      form.reset({
        name: objective.name,
        criteria: objective.criteria,
      });
    }
  }, [objective, form]);

  const onSubmit = async (data: UpdateSchema) => {
    if (!objective) return;

    try {
      await updateMutation.mutateAsync({
        projectId,
        objectiveId: objective.id,
        params: data,
      });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    onClose();
    form.reset();
    toast.success("Objective updated successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.objectives.all(projectId),
    });
  };

  return (
    <Dialog open={!!objective} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-lg sm:w-full">
        <DialogHeader>
          <DialogTitle>Edit Objective</DialogTitle>
          <DialogDescription className="hidden">
            Update the objective details
          </DialogDescription>
        </DialogHeader>
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
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="E.g., Contextual Adaptability"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="criteria"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Criteria</FormLabel>
                  <FormControl>
                    <Textarea
                      {...field}
                      className="min-h-40"
                      placeholder="E.g., Ability to maintain performance when task conditions, terminology, or input distributions change."
                      rows={6}
                    />
                  </FormControl>
                  <FormDescription>
                    This will be used to evaluate your LLM's performance.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button
                className="cursor-pointer"
                type="submit"
                disabled={updateMutation.isPending}
              >
                {updateMutation.isPending ? (
                  <Loader2Icon className="animate-spin" />
                ) : null}
                Save Changes
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
