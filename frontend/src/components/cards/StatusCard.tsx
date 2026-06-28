import { CheckCircle2, XCircle } from "lucide-react";

import { GlassCard } from "./GlassCard";

export const StatusCard = ({ title, online, detail }: { title: string; online: boolean; detail?: string }) => (
  <GlassCard>
    <div className="flex items-center gap-3">
      <div className={online ? "grid h-12 w-12 place-items-center rounded-2xl border border-success/20 bg-success/10 text-success" : "grid h-12 w-12 place-items-center rounded-2xl border border-danger/20 bg-danger/10 text-danger"}>
        {online ? <CheckCircle2 className="h-6 w-6" /> : <XCircle className="h-6 w-6" />}
      </div>
      <div>
        <p className="font-semibold">{title}</p>
        <p className="text-sm text-muted-foreground">{detail || (online ? "Online" : "Offline")}</p>
      </div>
    </div>
  </GlassCard>
);
