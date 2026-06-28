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
        <div key={String(item.career)} className="rounded-2xl border border-border bg-background/60 p-4 hover-lift">
          <div className="mb-3 flex items-center justify-between gap-3">
            <p className="font-semibold">{String(item.career || "-")}</p>
            <span className="rounded-full border border-primary/20 bg-primary/10 px-2.5 py-1 text-xs font-bold text-primary">{String(item.match_score || 0)}/100</span>
          </div>
          <p className="mt-1 text-sm text-muted-foreground">{String(item.why_it_fits || item.risk_or_gap || "")}</p>
        </div>
      ))}
    </div>
  </Card>
);
