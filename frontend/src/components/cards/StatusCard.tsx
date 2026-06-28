import { CheckCircle2, XCircle } from "lucide-react";

import { GlassCard } from "./GlassCard";

export const StatusCard = ({ title, online, detail }: { title: string; online: boolean; detail?: string }) => (
  <GlassCard>
    <div className="flex items-center gap-3">
      {online ? <CheckCircle2 className="h-6 w-6 text-success" /> : <XCircle className="h-6 w-6 text-danger" />}
      <div>
        <p className="font-semibold">{title}</p>
        <p className="text-sm text-muted-foreground">{detail || (online ? "Online" : "Offline")}</p>
      </div>
    </div>
  </GlassCard>
);
