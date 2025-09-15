"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { ArrowRightIcon, CheckIcon, Loader2Icon, PlusIcon } from "lucide-react";
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
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useCreateAgentMutation } from "@/data/create-agent-mutation";
import { queryKeys } from "@/data/query-keys";
import { ApiError } from "@/lib/api/client";

const createSchema = z.object({
  description: z.string().min(1, "Description is required").max(2000),
  name: z.string().min(1, "Name is required"),
});

type CreateSchema = z.infer<typeof createSchema>;

export interface CreateAgentDialogProps {
  projectId: string;
}

export function CreateAgentDialog({ projectId }: CreateAgentDialogProps) {
  const [open, setOpen] = React.useState<boolean>(false);
  const [showExample, setShowExample] = React.useState<boolean>(false);
  const createMutation = useCreateAgentMutation();
  const queryClient = useQueryClient();

  const form = useForm<CreateSchema>({
    resolver: zodResolver(createSchema),
    defaultValues: {
      name: "",
      description: "",
    },
  });

  React.useEffect(() => {
    if (!open) {
      form.reset();
      setShowExample(false);
    }
  }, [open, form]);

  const onSubmit = async (data: CreateSchema): Promise<void> => {
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
    toast.success("Agent created successfully");
    await queryClient.invalidateQueries({
      queryKey: queryKeys.agents.all(projectId),
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="cursor-pointer">
          <PlusIcon />
          New Agent
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md sm:w-full gap-0 p-0 overflow-hidden">
        <DialogHeader className="py-5 px-5">
          <DialogTitle>Create an Agent</DialogTitle>
          <DialogDescription className="hidden">
            Connect your agent to OneRun to start running simulations.
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
              <div>
                <Button
                  className="cursor-pointer w-full"
                  type="submit"
                  disabled={createMutation.isPending}
                >
                  {createMutation.isPending ? (
                    <Loader2Icon className="animate-spin" />
                  ) : null}
                  Create Agent
                  <ArrowRightIcon />
                </Button>
              </div>
            </form>
          </Form>
        </div>
        <div className="bg-background border-t px-5 py-6 flex flex-col gap-6">
          <div className="flex items-center justify-between gap-2">
            <div className="font-semibold">What to include</div>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setShowExample(!showExample)}
            >
              {showExample ? "Hide example" : "Show example"}
            </Button>
          </div>
          {showExample ? (
            <div className="flex flex-col gap-4">
              <div>
                <Label htmlFor="exampleName">Agent Name</Label>
                <div className="text-sm text-muted-foreground mt-1">
                  Finance AI Assistant
                </div>
              </div>
              <div>
                <Label htmlFor="exampleDescription">Agent Description</Label>
                <div className="text-sm text-muted-foreground mt-1">
                  Finara is an AI financial advisor designed to help users build
                  wealth, plan for major life goals, and achieve financial
                  independence.
                  <br />
                  <br />
                  Unlike static robo-advisors or manual budgeting tools, Finara
                  engages in dynamic, personalized conversations about
                  retirement planning, debt-reduction strategies, investment
                  opportunities, and creating sustainable budgets.
                  <br />
                  <br />
                  The AI is trained on sophisticated financial models to
                  understand market volatility, individual risk tolerance, and
                  the long-term implications of financial decisions.
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              {[
                {
                  id: "1",
                  title: "What does your agent do:",
                  description:
                    "Describe its core functionality and primary use case.",
                },
                {
                  id: "2",
                  title: "Who uses it, and when:",
                  description:
                    "Include user context, scenarios, or peak usage times.",
                },
                {
                  id: "3",
                  title: "Key features and capabilities:",
                  description:
                    "Highlight unique functionalities or integrations it offers.",
                },
              ].map(({ id, title, description }) => (
                <div key={id} className="flex items-center gap-4">
                  <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex justify-center items-center">
                    <CheckIcon className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-sm font-medium">{title}</div>
                    <div className="text-xs text-muted-foreground">
                      {description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
