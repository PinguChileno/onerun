"use client";

import type * as React from "react";
import { BotIcon, GavelIcon, SettingsIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { UserPopover } from "@/components/common/user-popover";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import { ProjectSelector } from "./project-selector";

export function ProjectNavbar(): React.JSX.Element {
  const pathname = usePathname();

  const isActive = (path: string): boolean => {
    return pathname.startsWith(path);
  };

  const activeClassName =
    "hover:bg-accent hover:text-accent-foreground bg-zinc-800 text-white";
  const inactiveClassName = "";

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background-2 backdrop-blur supports-[backdrop-filter]:bg-background-2">
      <div className="max-w-7xl mx-auto flex h-14 items-center justify-between">
        <div className="flex items-center gap-4">
          <Link className="inline-flex" href="/agents">
            <img
              alt="OneRun"
              loading="lazy"
              width="128"
              height="25"
              decoding="async"
              data-nimg="1"
              src="/assets/logo-dark.svg"
            />
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <Button
            className={cn(
              "cursor-pointer",
              isActive("/agents") ? activeClassName : inactiveClassName,
            )}
            variant="ghost"
            asChild
          >
            <Link href="/agents">
              <BotIcon />
              Agents
            </Link>
          </Button>
          <Button
            className={cn(
              "cursor-pointer",
              isActive("/objectives") ? activeClassName : inactiveClassName,
            )}
            variant="ghost"
            asChild
          >
            <Link href="/objectives">
              <GavelIcon />
              Objectives
            </Link>
          </Button>
          <Button
            className={cn(
              "cursor-pointer",
              isActive("/settings") ? activeClassName : inactiveClassName,
            )}
            variant="ghost"
            asChild
          >
            <Link href="/settings">
              <SettingsIcon />
              Settings
            </Link>
          </Button>
        </div>
        <div className="flex items-center gap-4">
          <ProjectSelector />
          <UserPopover />
        </div>
      </div>
    </header>
  );
}
