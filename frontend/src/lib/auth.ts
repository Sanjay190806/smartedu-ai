import type { UserProfile } from "./types";

interface GoogleJwtPayload {
  name?: string;
  email?: string;
  picture?: string;
}

export function decodeGoogleCredential(credential: string): UserProfile {
  const [, payload] = credential.split(".");
  const decoded = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/"))) as GoogleJwtPayload;
  return {
    name: decoded.name || "Google User",
    email: decoded.email || "google-user@smartedu.local",
    picture: decoded.picture,
    provider: "google",
  };
}

export const demoUser: UserProfile = {
  name: "Demo Student",
  email: "demo@smartedu.ai",
  provider: "demo",
};
