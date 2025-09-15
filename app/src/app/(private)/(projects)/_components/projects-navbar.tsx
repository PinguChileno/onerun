"use client";

import type * as React from "react";
import Link from "next/link";

import { UserPopover } from "@/components/common/user-popover";

export function ProjectNavbar(): React.JSX.Element {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background-2 backdrop-blur supports-[backdrop-filter]:bg-background-2">
      <div className="max-w-7xl mx-auto flex h-14 items-center justify-between">
        <Link className="inline-flex" href="/">
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
        <div className="flex items-center gap-2">
          <UserPopover />
        </div>
      </div>
    </header>
  );
}
