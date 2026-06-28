import { CareerFitChart } from "@/components/charts/CareerFitChart";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const CareerMatrix = ({ matrix }: { matrix: Array<Record<string, unknown>> }) => (
  <Card>
    <CardHeader>
      <CardTitle>Career Fit Matrix</CardTitle>
      <CardDescription>Comparison of candidate paths using interview signals.</CardDescription>
    </CardHeader>
    <CareerFitChart matrix={matrix} />
    <div className="mt-4 grid gap-3 md:grid-cols-2">
      {matrix.map((item) => (
        <div key={String(item.career)} className="rounded-xl border border-border bg-background/60 p-3">
          <p className="font-semibold">{String(item.career || "-")} <span className="text-primary">{String(item.match_score || 0)}/100</span></p>
          <p className="mt-1 text-sm text-muted-foreground">{String(item.why_it_fits || item.risk_or_gap || "")}</p>
        </div>
      ))}
    </div>
  </Card>
);
