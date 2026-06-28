import { useQuery } from "@tanstack/react-query";

import { CommandBox } from "@/components/common/CommandBox";
import { ErrorState } from "@/components/common/ErrorState";
import { StatusCard } from "@/components/cards/StatusCard";
import { PageShell } from "@/components/layout/PageShell";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

const routes = ["/health", "/students", "/predict", "/predict/batch", "/recommendations/{student_id}", "/analytics/summary", "/mentor/start", "/mentor/provider-status"];

export const SystemPage = () => {
  const health = useQuery({ queryKey: ["health"], queryFn: api.healthCheck });
  const provider = useQuery({ queryKey: ["provider-status"], queryFn: api.getMentorProviderStatus });
  return (
    <PageShell title="System Status" description="Backend health, provider status, routes, and local setup commands.">
      <div className="space-y-5">
        {health.isError ? <ErrorState message={(health.error as Error).message} /> : null}
        <div className="grid gap-4 md:grid-cols-2">
          <StatusCard title="FastAPI Backend" online={Boolean(health.data)} detail={String(health.data?.service || "Backend health")} />
          <StatusCard title="AI Provider" online={provider.data?.fallback_available ?? false} detail={`${provider.data?.provider || "offline"} · ${provider.data?.active_model || "offline-rule-based"}`} />
        </div>
        <Card><CardHeader><CardTitle>API Route Checklist</CardTitle></CardHeader><div className="grid gap-2 md:grid-cols-4">{routes.map((route) => <div key={route} className="rounded-xl border border-border bg-background/60 p-3 font-mono text-xs">{route}</div>)}</div></Card>
        <div className="grid gap-3 md:grid-cols-3">
          <CommandBox command="uvicorn backend.main:app --reload" />
          <CommandBox command="npm run dev" />
          <CommandBox command="python -m pytest" />
        </div>
      </div>
    </PageShell>
  );
};
