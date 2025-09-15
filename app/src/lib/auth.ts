import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { admin } from "better-auth/plugins/admin";
import { bearer } from "better-auth/plugins/bearer";
import { jwt } from "better-auth/plugins/jwt";
import { oneTimeToken } from "better-auth/plugins/one-time-token";

import { db } from "@/lib/db";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg" }),
  trustedOrigins: (process.env.BETTER_AUTH_TRUSTED_ORIGINS ?? "").split(","),
  baseURL: process.env.BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  plugins: [
    admin(),
    oneTimeToken(),
    bearer(),
    jwt({
      jwt: {
        issuer: process.env.BETTER_AUTH_JWT_ISSUER,
        audience: process.env.BETTER_AUTH_JWT_AUDIENCE,
        expirationTime: process.env.BETTER_AUTH_JWT_EXPIRATION_TIME,
      },
    }),
  ],
  advanced: {
    cookies: {
      session_token: {
        name: "session_token",
        attributes: {},
      },
    },
  },
  emailAndPassword: {
    enabled: true,
    disableSignUp: process.env.BETTER_AUTH_DISABLE_SIGNUP === "true",
  },
});
