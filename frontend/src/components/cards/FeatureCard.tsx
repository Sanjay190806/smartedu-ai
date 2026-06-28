import type { LucideIcon } from "lucide-react";

import { GlassCard } from "./GlassCard";

export const FeatureCard = ({ title, description, icon: Icon }: { title: string; description: string; icon: LucideIcon }) => (
  <GlassCard className="h-full">
    <Icon className="h-7 w-7 text-primary" />
    <h3 className="mt-4 text-lg font-semibold">{title}</h3>
    <p className="mt-2 text-sm leading-6 text-muted-foreground">{description}</p>
  </GlassCard>
);
