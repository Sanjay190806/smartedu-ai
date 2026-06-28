import { GoogleLogin } from "@react-oauth/google";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { BrainCircuit } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { GOOGLE_CLIENT_ID } from "@/lib/constants";
import { decodeGoogleCredential, demoUser } from "@/lib/auth";
import { useAuthStore } from "@/store/authStore";

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, login } = useAuthStore();
  const target = (location.state as { from?: string } | null)?.from || "/app/overview";

  if (isAuthenticated) return <Navigate to={target} replace />;

  return (
    <div className="app-bg grid min-h-screen place-items-center px-4">
      <div className="absolute right-4 top-4"><ThemeToggle /></div>
      <Card className="w-full max-w-md border-primary/20 bg-card/85 p-8">
        <div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-primary text-primary-foreground">
          <BrainCircuit className="h-7 w-7" />
        </div>
        <h1 className="mt-6 text-center text-3xl font-bold">Welcome to SmartEdu AI</h1>
        <p className="mt-2 text-center text-sm text-muted-foreground">Sign in with Google or continue in local demo mode.</p>
        <div className="mt-6 space-y-3">
          {GOOGLE_CLIENT_ID ? (
            <GoogleLogin
              onSuccess={(credentialResponse) => {
                if (credentialResponse.credential) {
                  login(decodeGoogleCredential(credentialResponse.credential));
                  navigate(target);
                }
              }}
              onError={() => undefined}
            />
          ) : (
            <ErrorState title="Google Auth not configured" message="Google Auth not configured. Use Demo Mode for local testing." />
          )}
          <Button
            className="w-full"
            size="lg"
            onClick={() => {
              login(demoUser);
              navigate(target);
            }}
          >
            Continue as Demo Student
          </Button>
        </div>
      </Card>
    </div>
  );
};
