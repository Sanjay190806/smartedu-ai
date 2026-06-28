import { useQuery } from "@tanstack/react-query";
import { Activity, BrainCircuit, CheckCircle2, Database, Globe2, Network, Server, TerminalSquare } from "lucide-react";

import { CommandBox } from "@/components/common/CommandBox";
import { ErrorState } from "@/components/common/ErrorState";
import { StatusCard } from "@/components/cards/StatusCard";
import { PageShell } from "@/components/layout/PageShell";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { API_BASE_URL } from "@/lib/constants";

const routes = ["/health", "/students", "/predict", "/predict/batch", "/recommendations/{student_id}", "/analytics/summary", "/mentor/start", "/mentor/provider-status"];

const architecture = [
  ["React UI", "Vite + TypeScript dashboard", Globe2],
  ["FastAPI", "Prediction and mentor APIs", Server],
  ["ML Registry", "Saved model artifacts", BrainCircuit],
  ["SQLite", "Local records and reports", Database],
] as const;

export const SystemPage = () => {
  const health = useQuery({ queryKey: ["health"], queryFn: api.healthCheck });
  const provider = useQuery({ queryKey: ["provider-status"], queryFn: api.getMentorProviderStatus });
  const providerData = provider.data;

  return (
    <PageShell title="System Status" description="Backend health, provider status, routes, local setup commands, and architecture notes.">
      <div className="space-y-5">
        {health.isError ? <ErrorState message={(health.error as Error).message} /> : null}

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatusCard title="FastAPI Backend" online={Boolean(health.data)} detail={String(health.data?.service || "Backend health")} />
          <StatusCard title="AI Provider" online={providerData?.fallback_available ?? false} detail={`${providerData?.provider || "offline"} - ${providerData?.active_model || "offline-rule-based"}`} />
          <StatusCard title="Local Database" online={Boolean(health.data)} detail="SQLite smartedu.db" />
          <StatusCard title="Frontend Runtime" online detail="React + Vite dashboard" />
        </div>

        <div className="grid gap-5 lg:grid-cols-[1fr_.9fr]">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Activity className="h-5 w-5 text-primary" /> API Route Checklist</CardTitle>
              <CardDescription>Core backend routes used by the React dashboard.</CardDescription>
            </CardHeader>
            <div className="grid gap-3 md:grid-cols-2">
              {routes.map((route) => (
                <div key={route} className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 p-3">
                  <CheckCircle2 className="h-4 w-4 text-success" />
                  <span className="font-mono text-xs">{route}</span>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Network className="h-5 w-5 text-primary" /> Local-First Architecture</CardTitle>
              <CardDescription>Everything needed for the demo runs from the repository root.</CardDescription>
            </CardHeader>
            <div className="grid gap-3">
              {architecture.map(([title, detail, Icon], index) => (
                <div key={title} className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 p-4">
                  <span className="grid h-9 w-9 place-items-center rounded-full bg-primary/10 text-xs font-bold text-primary">{index + 1}</span>
                  <Icon className="h-5 w-5 text-primary" />
                  <div>
                    <p className="font-semibold">{title}</p>
                    <p className="text-xs text-muted-foreground">{detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><TerminalSquare className="h-5 w-5 text-primary" /> Verification Commands</CardTitle>
            <CardDescription>Commands used to run the backend, frontend, and test suite.</CardDescription>
          </CardHeader>
          <div className="grid gap-3 md:grid-cols-3">
            <CommandBox command="uvicorn backend.main:app --reload" />
            <CommandBox command="npm run dev" />
            <CommandBox command="python -m pytest" />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Environment Status</CardTitle>
            <CardDescription>Frontend runtime values and provider guardrails.</CardDescription>
          </CardHeader>
          <div className="grid gap-3 md:grid-cols-3">
            <div className="kbd-card">API_BASE_URL={API_BASE_URL}</div>
            <div className="kbd-card">AI_PROVIDER={providerData?.provider || "offline"}</div>
            <div className="kbd-card">MODEL={providerData?.active_model || "offline-rule-based"}</div>
          </div>
          <p className="mt-4 text-sm leading-6 text-muted-foreground">
            Provider API keys must stay backend-side in `.env`. The React app only calls local FastAPI routes.
          </p>
        </Card>
      </div>
    </PageShell>
  );
};
