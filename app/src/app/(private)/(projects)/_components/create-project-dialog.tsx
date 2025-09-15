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
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useCreateProjectMutation } from "@/data/create-project-mutation";
import { queryKeys } from "@/data/query-keys";
import { ApiError } from "@/lib/api/client";

const createProjectSchema = z.object({
  name: z.string().min(1, "Name is required"),
});

type CreateProjectSchema = z.infer<typeof createProjectSchema>;

export function CreateProjectDialog() {
  const [open, setOpen] = React.useState<boolean>(false);
  const createMutation = useCreateProjectMutation();
  const queryClient = useQueryClient();

  const form = useForm<CreateProjectSchema>({
    resolver: zodResolver(createProjectSchema),
    defaultValues: {
      name: "",
    },
  });

  const onSubmit = async (data: CreateProjectSchema) => {
    try {
      await createMutation.mutateAsync(data);
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    setOpen(false);
    form.reset();
    toast.success("Project created successfully");
    await queryClient.invalidateQueries({ queryKey: queryKeys.projects.all() });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="cursor-pointer">
          <PlusIcon />
          New Project
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-lg sm:w-full">
        <DialogHeader>
          <DialogTitle>New Project</DialogTitle>
          <DialogDescription>
            Projects are used to organize agents and simulations.
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
                    <Input placeholder="Enter project name" {...field} />
                  </FormControl>
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
