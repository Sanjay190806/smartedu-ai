import type { LucideIcon } from "lucide-react";

import { GlassCard } from "./GlassCard";

export const FeatureCard = ({ title, description, icon: Icon }: { title: string; description: string; icon: LucideIcon }) => (
  <GlassCard className="h-full">
    <div className="grid h-12 w-12 place-items-center rounded-2xl border border-primary/20 bg-primary/10 text-primary">
      <Icon className="h-6 w-6" />
    </div>
    <h3 className="mt-4 text-lg font-semibold">{title}</h3>
    <p className="mt-2 text-sm leading-6 text-muted-foreground">{description}</p>
  </GlassCard>
);
