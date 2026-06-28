import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { BrainCircuit, Gauge, HeartPulse, ShieldCheck, UserRound } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { PageShell } from "@/components/layout/PageShell";
import { PredictionForm } from "@/components/prediction/PredictionForm";
import { PredictionResult } from "@/components/prediction/PredictionResult";
import { SampleProfiles } from "@/components/prediction/SampleProfiles";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { percent } from "@/lib/formatters";
import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";

export const PredictPage = () => {
  const [payload, setPayload] = useState<PredictionRequest>(sampleProfiles.medium);
  const mutation = useMutation({ mutationFn: api.predictStudent });
  const wellnessScore = Math.max(0, Math.min(100, ((payload.sleep_hours / 8) * 50) + ((10 - payload.stress_level) * 5)));
  const previewMetrics = [
    { label: "Attendance", value: percent(payload.attendance_percentage), score: payload.attendance_percentage, icon: ShieldCheck },
    { label: "Current GPA", value: `${payload.current_gpa}/10`, score: payload.current_gpa * 10, icon: Gauge },
    { label: "Assignment", value: percent(payload.assignment_completion_rate), score: payload.assignment_completion_rate, icon: BrainCircuit },
    { label: "Wellbeing", value: `${Math.round(wellnessScore)}%`, score: wellnessScore, icon: HeartPulse },
  ];

  return (
    <PageShell title="Risk Prediction" description="Run the saved Python ML model through FastAPI and receive explainable guidance.">
      <div className="grid gap-5 xl:grid-cols-[.78fr_1.22fr]">
        <aside className="space-y-5 xl:sticky xl:top-24 xl:self-start">
          <Card>
            <CardHeader>
              <CardTitle>Sample Profiles</CardTitle>
              <CardDescription>Load a realistic student profile, adjust values, then run the prediction.</CardDescription>
            </CardHeader>
            <SampleProfiles onSelect={setPayload} />
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Live Student Preview</CardTitle>
              <CardDescription>Current payload before it is submitted to `/predict`.</CardDescription>
            </CardHeader>
            <div className="space-y-3">
              <div className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 p-4">
                <div className="grid h-11 w-11 place-items-center rounded-2xl bg-primary/10 text-primary"><UserRound className="h-5 w-5" /></div>
                <div>
                  <p className="font-semibold">{payload.name}</p>
                  <p className="text-xs text-muted-foreground">{payload.student_id} - {payload.department}</p>
                </div>
              </div>
              {previewMetrics.map(({ label, value, score, icon: Icon }) => (
                <div key={label} className="rounded-2xl border border-border bg-background/60 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2">
                      <Icon className="h-4 w-4 text-primary" />
                      <p className="text-sm font-semibold">{label}</p>
                    </div>
                    <p className="font-bold">{value}</p>
                  </div>
                  <div className="metric-spark mt-3"><span style={{ width: `${Math.max(4, score)}%` }} /></div>
                </div>
              ))}
            </div>
          </Card>
        </aside>

        <div className="space-y-5">
          <Card>
            <CardHeader>
              <CardTitle>Prediction Workflow</CardTitle>
              <CardDescription>Grouped inputs mirror the dataset columns used by the trained models.</CardDescription>
            </CardHeader>
            <PredictionForm key={payload.student_id} value={payload} onChange={setPayload} onSubmit={(data) => mutation.mutate(data)} loading={mutation.isPending} />
          </Card>
          {mutation.isError ? <ErrorState message={(mutation.error as Error).message} /> : null}
          {mutation.data ? <PredictionResult result={mutation.data} /> : null}
        </div>
      </div>
    </PageShell>
  );
};
