import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const ProjectCards = ({ projects }: { projects: Array<Record<string, unknown>> }) => (
  <Card>
    <CardHeader>
      <CardTitle>Project Recommendations</CardTitle>
      <CardDescription>Portfolio-grade project options for GitHub and interviews.</CardDescription>
    </CardHeader>
    <div className="grid gap-4 md:grid-cols-2">
      {projects.map((project) => (
        <div key={String(project.project_title)} className="rounded-3xl border border-border bg-background/60 p-5 hover-lift">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">{String(project.difficulty || "Project")}</p>
          <h3 className="mt-2 text-lg font-semibold">{String(project.project_title || "-")}</h3>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">{String(project.why_this_project || "")}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {(Array.isArray(project.skills_used) ? project.skills_used : []).map((skill) => (
              <span key={String(skill)} className="premium-pill">{String(skill)}</span>
            ))}
          </div>
          {Array.isArray(project.deliverables) ? (
            <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
              {project.deliverables.map((item) => <li key={String(item)}>{String(item)}</li>)}
            </ul>
          ) : null}
          {project.github_value ? <p className="mt-4 rounded-2xl border border-primary/20 bg-primary/10 p-3 text-sm text-muted-foreground">{String(project.github_value)}</p> : null}
        </div>
      ))}
    </div>
  </Card>
);
