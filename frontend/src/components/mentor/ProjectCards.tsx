import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const ProjectCards = ({ projects }: { projects: Array<Record<string, unknown>> }) => (
  <Card>
    <CardHeader>
      <CardTitle>Project Recommendations</CardTitle>
      <CardDescription>Portfolio-grade project options for GitHub and interviews.</CardDescription>
    </CardHeader>
    <div className="grid gap-4 md:grid-cols-2">
      {projects.map((project) => (
        <div key={String(project.project_title)} className="rounded-2xl border border-border bg-background/60 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">{String(project.difficulty || "Project")}</p>
          <h3 className="mt-2 text-lg font-semibold">{String(project.project_title || "-")}</h3>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">{String(project.why_this_project || "")}</p>
          <p className="mt-3 text-xs text-muted-foreground">Skills: {Array.isArray(project.skills_used) ? project.skills_used.join(", ") : "-"}</p>
        </div>
      ))}
    </div>
  </Card>
);
