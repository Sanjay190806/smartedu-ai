import type { LucideIcon } from "lucide-react";

import { GlassCard } from "./GlassCard";

interface MetricCardProps {
  label: string;
  value: string | number;
  helper?: string;
  icon?: LucideIcon;
  progress?: number;
}

export const MetricCard = ({ label, value, helper, icon: Icon, progress }: MetricCardProps) => (
  <GlassCard>
    <div className="flex items-start justify-between">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">{label}</p>
        <div className="mt-3 text-3xl font-bold">{value}</div>
        {helper ? <p className="mt-2 text-sm text-muted-foreground">{helper}</p> : null}
      </div>
      {Icon ? (
        <div className="grid h-11 w-11 place-items-center rounded-2xl border border-primary/20 bg-primary/10 text-primary">
          <Icon className="h-5 w-5" />
        </div>
      ) : null}
    </div>
    {typeof progress === "number" ? (
      <div className="metric-spark mt-5">
        <span style={{ width: `${Math.max(4, Math.min(100, progress))}%` }} />
      </div>
    ) : null}
  </GlassCard>
);
