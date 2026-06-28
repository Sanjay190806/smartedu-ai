import { Download } from "lucide-react";

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

export const PredictionResult = ({ result }: { result: PredictionResponse }) => (
  <Card className="border-primary/30 bg-primary/5">
    <CardHeader>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <CardTitle className="flex items-center gap-3">Prediction Result <RiskBadge risk={result.risk_category} /></CardTitle>
          <CardDescription>{result.explanation}</CardDescription>
        </div>
        <Button variant="secondary" onClick={() => download(result)}>
          <Download className="h-4 w-4" /> Download JSON
        </Button>
      </div>
    </CardHeader>
    <div className="grid gap-4 md:grid-cols-3">
      <div className="rounded-xl border border-border bg-background/60 p-4">
        <p className="text-sm text-muted-foreground">Probability</p>
        <p className="mt-1 text-2xl font-bold">{percent(result.probability)}</p>
      </div>
      <div className="rounded-xl border border-border bg-background/60 p-4">
        <p className="text-sm text-muted-foreground">Confidence</p>
        <p className="mt-1 text-2xl font-bold">{result.confidence}</p>
      </div>
      <div className="rounded-xl border border-border bg-background/60 p-4">
        <p className="text-sm text-muted-foreground">Recommendation</p>
        <p className="mt-1 text-sm">{result.recommendations.summary}</p>
      </div>
    </div>
    <div className="mt-5 grid gap-4 lg:grid-cols-2">
      {[
        ["Top Factors", result.top_factors],
        ["Action Plan", result.recommendations.action_plan],
        ["7-Day Plan", result.recommendations.seven_day_plan],
        ["30-Day Plan", result.recommendations.thirty_day_plan],
      ].map(([title, items]) => (
        <div key={title as string} className="rounded-xl border border-border bg-background/60 p-4">
          <p className="font-semibold">{title as string}</p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted-foreground">
            {(items as string[]).map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      ))}
    </div>
    <p className="mt-5 rounded-xl border border-border bg-background/60 p-4 text-sm text-muted-foreground">{result.recommendations.mentor_note}</p>
  </Card>
);
