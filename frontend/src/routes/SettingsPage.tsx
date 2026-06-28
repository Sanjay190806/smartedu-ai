import { API_BASE_URL, GOOGLE_CLIENT_ID } from "@/lib/constants";
import { useAppStore } from "@/store/appStore";
import { useAuthStore } from "@/store/authStore";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export const SettingsPage = () => {
  const { theme, setTheme } = useAppStore();
  const { user } = useAuthStore();
  return (
    <PageShell title="Settings" description="Local frontend settings, auth state, provider notes, and security reminders.">
      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Theme</CardTitle></CardHeader>
          <div className="flex gap-2">
            <Button variant={theme === "dark" ? "default" : "secondary"} onClick={() => setTheme("dark")}>Dark</Button>
            <Button variant={theme === "light" ? "default" : "secondary"} onClick={() => setTheme("light")}>Light</Button>
          </div>
        </Card>
        <Card>
          <CardHeader><CardTitle>Auth State</CardTitle></CardHeader>
          <p className="text-sm text-muted-foreground">Signed in as {user?.name || "Unknown"} via {user?.provider || "none"}.</p>
          <p className="mt-2 text-sm text-muted-foreground">Google Client ID: {GOOGLE_CLIENT_ID ? "Configured" : "Not configured; demo mode available"}</p>
        </Card>
        <Card>
          <CardHeader><CardTitle>API Base URL</CardTitle></CardHeader>
          <p className="font-mono text-sm text-muted-foreground">{API_BASE_URL}</p>
        </Card>
        <Card>
          <CardHeader><CardTitle>Security Note</CardTitle></CardHeader>
          <p className="text-sm leading-6 text-muted-foreground">OpenRouter and Groq API keys must stay backend-side in `.env`. Never expose provider API keys in React environment variables.</p>
        </Card>
      </div>
    </PageShell>
  );
};
