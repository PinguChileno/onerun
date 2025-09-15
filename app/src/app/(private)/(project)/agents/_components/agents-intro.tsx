import type * as React from "react";
import { CodeIcon, ExternalLinkIcon, SortAscIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function AgentsIntro(): React.JSX.Element {
  return (
    <div className="flex-1 flex flex-col items-center justify-center">
      <Card className="max-w-md w-full overflow-hidden">
        <div className="h-[200px] flex flex-col items-center justify-center bg-background-3">
          <img src="/assets/users-group.svg" alt="Users Group" />
        </div>
        <div className="flex flex-col gap-6 px-6 py-8">
          <div className="flex flex-col gap-1">
            <div className="text-xl font-semibold">
              Introducing Simulation Agents
            </div>
            <div className="text-sm text-muted-foreground">
              All work simulations in OneRun require an active connection to the
              chatbot you want to simulate.
            </div>
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex flex-shrink-0 justify-center items-center">
                <SortAscIcon className="h-4 w-4" />
              </div>
              <div className="text-sm text-muted-foreground">
                Maximum flexibility, full customization, local development
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex flex-shrink-0 justify-center items-center">
                <CodeIcon className="h-4 w-4" />
              </div>
              <div className="text-sm text-muted-foreground">
                Requires technical knowledge, more setup time
              </div>
            </div>
          </div>
        </div>
        <div className="flex justify-end pb-2 px-2">
          <Button variant="secondary" size="sm" asChild>
            <a
              href="https://docs.onerun.ai/concepts/agents"
              rel="noreferrer"
              target="_blank"
            >
              Read docs
              <ExternalLinkIcon />
            </a>
          </Button>
        </div>
      </Card>
    </div>
  );
}
