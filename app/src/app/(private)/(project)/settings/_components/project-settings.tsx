"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { Waveform } from "ldrs/react";
import { CheckCircleIcon, CopyIcon, Loader2Icon } from "lucide-react";
import { ApiError } from "next/dist/server/api-utils";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { useGetProjectQuery } from "@/data/get-project-query";
import { queryKeys } from "@/data/query-keys";
import { useUpdateProjectMutation } from "@/data/update-project-mutation";
import { useCopy } from "@/hooks/use-copy";

const updateSchema = z.object({
  name: z.string().min(1, "Name is required"),
});

type UpdateSchema = z.infer<typeof updateSchema>;

export interface ProjectSettingsProps {
  projectId: string;
}

export function ProjectSettings({
  projectId,
}: ProjectSettingsProps): React.JSX.Element | null {
  const { data: project, error, isLoading } = useGetProjectQuery(projectId);
  const updateMutation = useUpdateProjectMutation();
  const queryClient = useQueryClient();
  const { copy, copied } = useCopy();

  const form = useForm<UpdateSchema>({
    resolver: zodResolver(updateSchema),
    defaultValues: {
      name: "",
    },
  });

  React.useEffect(() => {
    if (project) {
      form.reset({
        name: project.name,
      });
    }
  }, [project, form]);

  const onSubmit = async (data: UpdateSchema): Promise<void> => {
    try {
      await updateMutation.mutateAsync({ projectId, params: data });
    } catch (err) {
      console.error(err);
      const msg =
        err instanceof ApiError ? err.message : "Something went wrong";
      toast.error(msg);
      return;
    }

    form.reset();
    toast.success("Project updated successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.projects.all(),
    });
  };

  const renderContent = (): React.JSX.Element | null => {
    if (isLoading) {
      return <Loading />;
    }

    if (error) {
      return <ErrorDisplay message={error.message} />;
    }

    if (!project) {
      return null;
    }

    return (
      <Card>
        <CardContent className="p-6">
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex flex-col gap-4 max-w-xl"
            >
              <div className="flex flex-col gap-2 gap-2">
                <Label htmlFor="projectId">Project ID</Label>
                <div className="flex gap-2">
                  <Input
                    type="text"
                    id="projectId"
                    value={project.id}
                    readOnly
                    className="cursor-default text-muted-foreground focus-visible:ring-0"
                  />
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        className="cursor-pointer"
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={() => copy(project.id)}
                      >
                        {copied ? <CheckCircleIcon /> : <CopyIcon />}
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Copy</TooltipContent>
                  </Tooltip>
                </div>
              </div>
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
              <div className="justify-end flex gap-4">
                {form.formState.isDirty ? (
                  <Button
                    onClick={() => form.reset()}
                    type="button"
                    variant="outline"
                    disabled={updateMutation.isPending}
                  >
                    Cancel
                  </Button>
                ) : null}
                <Button type="submit" disabled={updateMutation.isPending}>
                  {updateMutation.isPending ? (
                    <Loader2Icon className="animate-spin" />
                  ) : null}
                  Save Changes
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    );
  };

  return renderContent();
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
