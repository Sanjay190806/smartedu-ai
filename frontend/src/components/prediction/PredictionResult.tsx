import { AlertTriangle, BookOpen, CalendarDays, CheckCircle2, Download, ListChecks, MessageSquare, Target } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { RiskBadge } from "@/components/cards/RiskBadge";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { percent } from "@/lib/formatters";
import type { PredictionResponse } from "@/lib/types";

function download(payload: PredictionResponse) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${payload.student_id || "student"}-prediction.json`;
  link.click();
  URL.revokeObjectURL(url);
}

const riskCopy: Record<string, string> = {
  "Low Risk": "Student appears academically stable. Continue momentum and maintain healthy study rhythm.",
  "Medium Risk": "Student needs focused monitoring and short-cycle support before risk escalates.",
  "High Risk": "Student needs immediate mentor attention, academic recovery support, and wellbeing check-in.",
};

const InsightList = ({ title, icon: Icon, items }: { title: string; icon: LucideIcon; items: string[] }) => (
  <div className="rounded-3xl border border-border bg-background/60 p-4">
    <div className="mb-3 flex items-center gap-2">
      <div className="grid h-9 w-9 place-items-center rounded-xl bg-primary/10 text-primary"><Icon className="h-4 w-4" /></div>
      <p className="font-semibold">{title}</p>
    </div>
    <ul className="space-y-2 text-sm text-muted-foreground">
      {items.map((item) => (
        <li key={item} className="flex gap-2">
          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  </div>
);

export const PredictionResult = ({ result }: { result: PredictionResponse }) => {
  const probability = result.probability <= 1 ? result.probability * 100 : result.probability;
  const ringStyle = { background: `conic-gradient(hsl(var(--primary)) ${probability}%, hsl(var(--muted)) 0)` };

  return (
    <Card className="overflow-hidden border-primary/30 bg-primary/5">
      <div className="grid gap-5 lg:grid-cols-[.88fr_1.12fr]">
        <div className="rounded-[1.75rem] border border-border bg-background/70 p-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="section-eyebrow">Prediction result</p>
              <CardTitle className="mt-2 flex items-center gap-3 text-2xl">
                {result.risk_category} <RiskBadge risk={result.risk_category} />
              </CardTitle>
              <CardDescription className="mt-2">{riskCopy[result.risk_category] || result.explanation}</CardDescription>
            </div>
            <Button variant="secondary" onClick={() => download(result)}>
              <Download className="h-4 w-4" /> JSON
            </Button>
          </div>
          <div className="mt-6 grid gap-4 sm:grid-cols-[auto_1fr]">
            <div className="grid h-36 w-36 place-items-center rounded-full p-2" style={ringStyle}>
              <div className="grid h-full w-full place-items-center rounded-full bg-card text-center">
                <div>
                  <p className="text-3xl font-bold">{percent(result.probability)}</p>
                  <p className="text-xs text-muted-foreground">probability</p>
                </div>
              </div>
            </div>
            <div className="space-y-3">
              <div className="rounded-2xl border border-border bg-card/70 p-4">
                <p className="text-xs text-muted-foreground">Confidence</p>
                <p className="mt-1 text-2xl font-bold">{result.confidence}</p>
              </div>
              <div className="rounded-2xl border border-border bg-card/70 p-4">
                <p className="text-xs text-muted-foreground">Human explanation</p>
                <p className="mt-2 text-sm leading-6">{result.explanation}</p>
              </div>
            </div>
          </div>
          <div className="mt-5 rounded-3xl border border-warning/25 bg-warning/10 p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-warning" />
              <div>
                <p className="font-semibold">Recommendation summary</p>
                <p className="mt-1 text-sm leading-6 text-muted-foreground">{result.recommendations.summary}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <CardHeader className="mb-0 p-0">
            <CardTitle>Guidance Pack</CardTitle>
            <CardDescription>Factors, intervention tasks, resources, and mentor note persisted by the backend.</CardDescription>
          </CardHeader>
          <div className="grid gap-4 md:grid-cols-2">
            <InsightList title="Top Factors" icon={Target} items={result.top_factors} />
            <InsightList title="Top Problems" icon={AlertTriangle} items={result.recommendations.top_problems} />
            <InsightList title="Action Plan" icon={ListChecks} items={result.recommendations.action_plan} />
            <InsightList title="7-Day Timeline" icon={CalendarDays} items={result.recommendations.seven_day_plan} />
            <InsightList title="30-Day Roadmap" icon={Target} items={result.recommendations.thirty_day_plan} />
            <InsightList title="Resources" icon={BookOpen} items={result.recommendations.resources} />
          </div>
          <div className="rounded-3xl border border-primary/20 bg-primary/10 p-4">
            <div className="mb-2 flex items-center gap-2 font-semibold">
              <MessageSquare className="h-4 w-4 text-primary" /> Mentor note
            </div>
            <p className="text-sm leading-6 text-muted-foreground">{result.recommendations.mentor_note}</p>
          </div>
        </div>
      </div>
    </Card>
  );
};
