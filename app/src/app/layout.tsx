import type { Metadata } from "next";

import "ldrs/react/Waveform.css";
import "@/styles/globals.css";

import { Toaster } from "@/components/ui/sonner";
import { geistMono, geistSans } from "@/lib/fonts";
import { AuthProvider } from "@/providers/auth-provider";
import { QueryClientProvider } from "@/providers/query-client-provider";

export const metadata: Metadata = {
  title: "OneRun.ai",
  description: "OneRun - all-in-one solution to evaluate your AI agents",
};

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <QueryClientProvider>
          <AuthProvider>
            {children}
            <Toaster />
          </AuthProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
