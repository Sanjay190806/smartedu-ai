import { ClipboardCheck, ShieldAlert } from "lucide-react";

import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const riskTone: Record<string, string> = {
  low: "border-success/25 bg-success/10 text-success",
  medium: "border-warning/25 bg-warning/10 text-warning",
  high: "border-danger/25 bg-danger/10 text-danger",
};

export const SampleProfiles = ({ onSelect }: { onSelect: (payload: PredictionRequest) => void }) => (
  <div className="grid gap-3">
    {Object.entries(sampleProfiles).map(([key, payload]) => (
      <Card key={key} className="p-4 hover-lift">
        <div className="flex items-start justify-between gap-3">
          <div>
            <span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-bold ${riskTone[key] || "border-primary/25 bg-primary/10 text-primary"}`}>
              {key} sample
            </span>
            <h3 className="mt-3 font-semibold">{payload.name}</h3>
            <p className="mt-1 text-sm text-muted-foreground">{payload.department} batch profile</p>
          </div>
          <ShieldAlert className="h-5 w-5 text-primary" />
        </div>
        <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
          <div className="rounded-xl border border-border bg-background/60 p-2">
            <p className="text-muted-foreground">Attendance</p>
            <p className="font-bold">{payload.attendance_percentage}%</p>
          </div>
          <div className="rounded-xl border border-border bg-background/60 p-2">
            <p className="text-muted-foreground">GPA</p>
            <p className="font-bold">{payload.current_gpa}/10</p>
          </div>
          <div className="rounded-xl border border-border bg-background/60 p-2">
            <p className="text-muted-foreground">Backlogs</p>
            <p className="font-bold">{payload.backlogs}</p>
          </div>
        </div>
        <Button variant="secondary" size="sm" className="mt-4 w-full" onClick={() => onSelect(payload)}>
          <ClipboardCheck className="h-4 w-4" /> Load Sample
        </Button>
      </Card>
    ))}
  </div>
);
