import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { titleCase } from "@/lib/formatters";

export const WeeklyPlan = ({ plan }: { plan: Record<string, string[]> }) => (
  <Card>
    <CardHeader>
      <CardTitle>Weekly Plan</CardTitle>
      <CardDescription>Repeatable cadence for execution.</CardDescription>
    </CardHeader>
    <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
      {Object.entries(plan || {}).map(([day, tasks]) => (
        <div key={day} className="rounded-xl border border-border bg-background/60 p-3">
          <p className="font-semibold">{titleCase(day)}</p>
          <p className="mt-2 text-sm text-muted-foreground">{tasks.join(", ")}</p>
        </div>
      ))}
    </div>
  </Card>
);
