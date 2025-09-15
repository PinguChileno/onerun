import type * as React from "react";
import Link from "next/link";

import { LoginForm } from "./_components/login-form";

interface PageProps {
  searchParams: Promise<{ return_to?: string }>;
}

export default async function Page({
  searchParams,
}: PageProps): Promise<React.JSX.Element> {
  const { return_to } = await searchParams;
  const returnTo = return_to || "/";

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="max-w-lg w-full flex flex-col gap-8">
        <div className="flex justify-center">
          <Link className="inline-flex" href="/">
            <img
              alt="OneRun"
              loading="lazy"
              width="154"
              height="30"
              decoding="async"
              data-nimg="1"
              src="/assets/logo-dark.svg"
            />
          </Link>
        </div>
        <LoginForm returnTo={returnTo} />
        <div className="text-sm text-muted-foreground text-center">
          © 2025 OneRun.ai
        </div>
      </div>
    </div>
  );
}
