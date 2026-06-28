import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { titleCase } from "@/lib/formatters";

export const SkillRoadmap = ({ roadmap }: { roadmap: Record<string, unknown> }) => (
  <Card>
    <CardHeader>
      <CardTitle>Skill Roadmap</CardTitle>
      <CardDescription>30/60/90 day execution plan.</CardDescription>
    </CardHeader>
    <div className="grid gap-3 md:grid-cols-2">
      {Object.entries(roadmap || {}).map(([key, value]) => (
        <div key={key} className="rounded-xl border border-border bg-background/60 p-4">
          <p className="font-semibold">{titleCase(key)}</p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">{Array.isArray(value) ? value.join(", ") : String(value)}</p>
        </div>
      ))}
    </div>
  </Card>
);
