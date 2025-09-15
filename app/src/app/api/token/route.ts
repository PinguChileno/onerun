import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";

export async function GET(request: NextRequest) {
  try {
    // Get the session from the request
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session) {
      return NextResponse.json({ error: "No active session" }, { status: 401 });
    }

    // Generate a JWT token for the session using better-auth's JWT plugin
    const token = await auth.api.signJWT({
      body: {
        payload: {
          userId: session.user.id,
          sessionId: session.session.id,
        },
      },
    });

    return NextResponse.json({ token });
  } catch (error) {
    console.error("Token generation error:", error);
    return NextResponse.json(
      { error: "Failed to generate token" },
      { status: 500 },
    );
  }
}
