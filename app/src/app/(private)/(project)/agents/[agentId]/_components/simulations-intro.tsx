import type * as React from "react";
import {
  CodeIcon,
  ExternalLinkIcon,
  SortAscIcon,
  SquareUserIcon,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function SimulationsIntro(): React.JSX.Element {
  return (
    <div className="flex-1 flex flex-col items-center justify-center">
      <Card className="max-w-md w-full overflow-hidden">
        <div className="h-[200px] flex flex-col items-center justify-center bg-background-3">
          <img src="/assets/validation.svg" alt="Validation" />
        </div>
        <div className="flex flex-col gap-6 px-6 py-8">
          <div className="flex flex-col gap-1">
            <div className="text-xl font-semibold">
              Realistic AI Simulations
            </div>
            <div className="text-sm text-muted-foreground">
              Generate targeted conversations to see how your AI performs. You
              define the users and their goals to control the focus of every
              test.
            </div>
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex flex-shrink-0 justify-center items-center">
                <SortAscIcon className="h-4 w-4" />
              </div>
              <div className="text-sm text-muted-foreground">
                <span className="text-foreground font-semibold">
                  Target Scenarios:
                </span>{" "}
                Pinpoint and test a specific feature, workflow, or bug.
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex flex-shrink-0 justify-center items-center">
                <CodeIcon className="h-4 w-4" />
              </div>
              <div className="text-sm text-muted-foreground">
                <span className="text-foreground font-semibold">
                  Explore Broadly:
                </span>{" "}
                Test general topics with diverse users to find unexpected
                issues.
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="rounded-full bg-accent text-accent-foreground h-9 w-9 flex flex-shrink-0 justify-center items-center">
                <SquareUserIcon className="h-4 w-4" />
              </div>
              <div className="text-sm text-muted-foreground">
                <span className="text-foreground font-semibold">
                  Simulate Behaviors:
                </span>{" "}
                Stress-test your AI with personalities like 'impatient' or
                'skeptical'.
              </div>
            </div>
          </div>
        </div>
        <div className="flex justify-end pb-2 px-2">
          <Button variant="secondary" size="sm" asChild>
            <a
              href="https://docs.onerun.ai/concepts/simulation"
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
