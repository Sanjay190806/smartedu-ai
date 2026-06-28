import { Moon, ShieldCheck, Sparkles, Sun, UserRound } from "lucide-react";

import { API_BASE_URL, GOOGLE_CLIENT_ID } from "@/lib/constants";
import { useAppStore } from "@/store/appStore";
import { useAuthStore } from "@/store/authStore";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const securityNotes = [
  { title: "Backend only", copy: "Provider keys must stay in backend `.env`, never in React environment variables.", icon: ShieldCheck },
  { title: "Demo safe", copy: "The app supports local demo auth when Google OAuth is not configured.", icon: Sparkles },
  { title: "Local data", copy: "SQLite keeps this portfolio demo easy to run from the repository root.", icon: ShieldCheck },
];

export const SettingsPage = () => {
  const { theme, setTheme } = useAppStore();
  const { user } = useAuthStore();

  return (
    <PageShell title="Settings" description="Local frontend settings, auth state, provider notes, and security reminders.">
      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Theme Experience</CardTitle>
            <CardDescription>Switch between AI command-center dark mode and clean SaaS light mode.</CardDescription>
          </CardHeader>
          <div className="grid gap-3 sm:grid-cols-2">
            <button
              className={theme === "dark" ? "rounded-3xl border border-primary/30 bg-primary/10 p-5 text-left ring-2 ring-primary/30" : "rounded-3xl border border-border bg-background/60 p-5 text-left transition hover:border-primary/30"}
              onClick={() => setTheme("dark")}
            >
              <Moon className="h-6 w-6 text-primary" />
              <p className="mt-4 font-semibold">Dark Command</p>
              <p className="mt-1 text-sm text-muted-foreground">Futuristic academic intelligence workspace.</p>
            </button>
            <button
              className={theme === "light" ? "rounded-3xl border border-primary/30 bg-primary/10 p-5 text-left ring-2 ring-primary/30" : "rounded-3xl border border-border bg-background/60 p-5 text-left transition hover:border-primary/30"}
              onClick={() => setTheme("light")}
            >
              <Sun className="h-6 w-6 text-primary" />
              <p className="mt-4 font-semibold">Light SaaS</p>
              <p className="mt-1 text-sm text-muted-foreground">Clean, presentation-ready product dashboard.</p>
            </button>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Auth State</CardTitle>
            <CardDescription>Current frontend session identity.</CardDescription>
          </CardHeader>
          <div className="rounded-3xl border border-border bg-background/60 p-5">
            <div className="flex items-center gap-3">
              {user?.picture ? <img src={user.picture} alt="" className="h-12 w-12 rounded-2xl" /> : <div className="grid h-12 w-12 place-items-center rounded-2xl bg-primary/10 text-primary"><UserRound className="h-6 w-6" /></div>}
              <div>
                <p className="font-semibold">{user?.name || "Unknown"}</p>
                <p className="text-sm text-muted-foreground">{user?.email || "No email"} - {user?.provider || "none"}</p>
              </div>
            </div>
            <p className="mt-4 text-sm text-muted-foreground">Google Client ID: {GOOGLE_CLIENT_ID ? "Configured" : "Not configured; demo mode available"}</p>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>API Base URL</CardTitle>
            <CardDescription>React calls this local FastAPI base URL.</CardDescription>
          </CardHeader>
          <div className="kbd-card text-sm">{API_BASE_URL}</div>
          <Button className="mt-4" variant="secondary" onClick={() => navigator.clipboard?.writeText(API_BASE_URL)}>
            Copy URL
          </Button>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Provider and Security Notes</CardTitle>
            <CardDescription>Guardrails for OpenRouter/Groq optional AI provider usage.</CardDescription>
          </CardHeader>
          <div className="space-y-3">
            {securityNotes.map(({ title, copy, icon: Icon }) => (
              <div key={title} className="flex gap-3 rounded-2xl border border-border bg-background/60 p-4">
                <Icon className="mt-0.5 h-5 w-5 text-primary" />
                <div>
                  <p className="font-semibold">{title}</p>
                  <p className="text-sm leading-6 text-muted-foreground">{copy}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </PageShell>
  );
};
