"use client";

import * as React from "react";

import { client } from "@/lib/api/client";
import { authClient } from "@/lib/auth-client";

export interface User {
  id: string;
  email: string;
  name: string;
  // Add other user properties as needed
}

export interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  refreshAuth: () => Promise<void>;
}

export const AuthContext = React.createContext<AuthContextType | undefined>(
  undefined,
);

export function useAuth() {
  const context = React.useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

// Convenience hook for just user data
export function useUser() {
  const { user } = useAuth();
  return user;
}

// Convenience hook for authentication status
export function useIsAuthenticated() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated;
}

export interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [isAuthenticated, setIsAuthenticated] = React.useState<boolean>(false);
  const [isLoading, setIsLoading] = React.useState<boolean>(true);
  const [user, setUser] = React.useState<User | null>(null);

  const refreshAuth = React.useCallback(async () => {
    try {
      setIsLoading(true);

      // Check if user has an active session with better-auth
      const session = await authClient.getSession();

      if (session.data) {
        setIsAuthenticated(true);
        setUser(session.data.user as User);
        // Clear any existing token to force refresh
        client.clearToken();
      } else {
        setIsAuthenticated(false);
        setUser(null);
        client.clearToken();
      }
    } catch (error) {
      console.error("Auth refresh error:", error);
      setIsAuthenticated(false);
      setUser(null);
      client.clearToken();
    } finally {
      setIsLoading(false);
    }
  }, []);

  React.useEffect(() => {
    refreshAuth();
  }, [refreshAuth]);

  // Poll for session changes periodically
  React.useEffect(() => {
    const interval = setInterval(() => {
      authClient.getSession().then((session) => {
        const wasAuthenticated = isAuthenticated;
        const nowAuthenticated = !!session.data;

        if (wasAuthenticated !== nowAuthenticated) {
          setIsAuthenticated(nowAuthenticated);
          setUser(nowAuthenticated ? (session.data?.user as User) : null);
          if (!nowAuthenticated) {
            client.clearToken();
          }
        }
      });
    }, 15000); // Check every 15 seconds

    return () => clearInterval(interval);
  }, [isAuthenticated]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isLoading,
        user,
        refreshAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
