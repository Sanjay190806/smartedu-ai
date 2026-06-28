import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export const SampleProfiles = ({ onSelect }: { onSelect: (payload: PredictionRequest) => void }) => (
  <div className="grid gap-3 md:grid-cols-3">
    {Object.entries(sampleProfiles).map(([key, payload]) => (
      <Card key={key} className="space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">{key} sample</p>
        <h3 className="font-semibold">{payload.name}</h3>
        <p className="text-sm text-muted-foreground">Attendance {payload.attendance_percentage}% · GPA {payload.current_gpa}/10 · Backlogs {payload.backlogs}</p>
        <Button variant="secondary" size="sm" onClick={() => onSelect(payload)}>Load Sample</Button>
      </Card>
    ))}
  </div>
);
