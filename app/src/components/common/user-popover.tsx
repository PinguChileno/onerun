"use client";

import * as React from "react";
import { Loader2Icon, LogOutIcon, UserIcon } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { authClient } from "@/lib/auth-client";
import { useAuth, useUser } from "@/providers/auth-provider";

export function UserPopover(): React.JSX.Element {
  const user = useUser();
  const { isLoading } = useAuth();
  const [isSigningOut, setIsSigningOut] = React.useState<boolean>(false);

  const handleSignOut = async () => {
    try {
      setIsSigningOut(true);
      await authClient.signOut();
      window.location.href = "/login";
    } catch (error) {
      console.error("Sign out error:", error);
      toast.error("Failed to sign out. Please try again.");
      setIsSigningOut(false);
    }
  };

  const getUserInitials = (name?: string, email?: string): string => {
    if (name) {
      return name
        .split(" ")
        .map((part) => part[0])
        .slice(0, 2)
        .join("")
        .toUpperCase();
    }
    if (email) {
      return email[0].toUpperCase();
    }
    return "U";
  };

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          className="cursor-pointer h-8 w-8 rounded-full"
          variant="outline"
          size="sm"
        >
          {user ? (
            <span className="text-xs font-medium">
              {getUserInitials(user.name, user.email)}
            </span>
          ) : (
            <UserIcon />
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-64" align="end">
        {isLoading ? (
          <div className="text-sm text-muted-foreground">Loading...</div>
        ) : user ? (
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-1">
              <h4 className="font-medium leading-none">
                {user.name || "User"}
              </h4>
              <p className="text-sm text-muted-foreground">{user.email}</p>
            </div>
            <div className="border-t pt-3">
              <Button
                variant="ghost"
                className="cursor-pointer w-full justify-start text-destructive hover:text-destructive hover:bg-destructive/10"
                onClick={handleSignOut}
                disabled={isSigningOut}
              >
                <LogOutIcon />
                Sign Out
                {isSigningOut ? <Loader2Icon className="animate-spin" /> : null}
              </Button>
            </div>
          </div>
        ) : (
          <div className="text-sm text-muted-foreground">Not signed in</div>
        )}
      </PopoverContent>
    </Popover>
  );
}
