import type { LucideIcon } from "lucide-react";

import { GlassCard } from "./GlassCard";

interface MetricCardProps {
  label: string;
  value: string | number;
  helper?: string;
  icon?: LucideIcon;
}

export const MetricCard = ({ label, value, helper, icon: Icon }: MetricCardProps) => (
  <GlassCard>
    <div className="flex items-start justify-between">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">{label}</p>
        <div className="mt-3 text-3xl font-bold">{value}</div>
        {helper ? <p className="mt-2 text-sm text-muted-foreground">{helper}</p> : null}
      </div>
      {Icon ? <Icon className="h-6 w-6 text-primary" /> : null}
    </div>
  </GlassCard>
);
