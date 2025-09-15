"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { Loader2Icon, PlusIcon } from "lucide-react";
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
  DialogTrigger,
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
import { useCreateObjectiveMutation } from "@/data/create-objective-mutation";
import { queryKeys } from "@/data/query-keys";
import { ApiError } from "@/lib/api/client";

const createSchema = z.object({
  name: z.string().min(1, "Name is required"),
  criteria: z.string().min(1, "Criteria is required"),
});

type CreateSchema = z.infer<typeof createSchema>;

export interface CreateObjectiveDialogProps {
  projectId: string;
}

export function CreateObjectiveDialog({
  projectId,
}: CreateObjectiveDialogProps) {
  const [open, setOpen] = React.useState<boolean>(false);
  const createMutation = useCreateObjectiveMutation();
  const queryClient = useQueryClient();

  const form = useForm<CreateSchema>({
    resolver: zodResolver(createSchema),
    defaultValues: {
      name: "",
      criteria: "",
    },
  });

  const onSubmit = async (data: CreateSchema) => {
    try {
      await createMutation.mutateAsync({ projectId, params: data });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    setOpen(false);
    form.reset();
    toast.success("Objective created successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.objectives.all(projectId),
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="cursor-pointer">
          <PlusIcon />
          New Objective
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-lg sm:w-full">
        <DialogHeader>
          <DialogTitle>New Objective</DialogTitle>
          <DialogDescription className="hidden">
            Create a new evaluation objective
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
                disabled={createMutation.isPending}
              >
                {createMutation.isPending ? (
                  <Loader2Icon className="animate-spin" />
                ) : null}
                Create
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
