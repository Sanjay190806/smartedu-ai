import { CareerMatrix } from "./CareerMatrix";
import { ProjectCards } from "./ProjectCards";
import { ReportDownload } from "./ReportDownload";
import { SkillRoadmap } from "./SkillRoadmap";
import { WeeklyPlan } from "./WeeklyPlan";

import { ReadinessScoreChart } from "@/components/charts/ReadinessScoreChart";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { MentorReport as MentorReportType } from "@/lib/types";

const record = (value: unknown) => (typeof value === "object" && value !== null ? (value as Record<string, unknown>) : {});

export const MentorReport = ({ payload }: { payload: MentorReportType }) => {
  const report = payload.report;
  const executive = record(report.executive_summary);
  const career = record(report.career_path_recommendation);
  const trace = record(report.career_reasoning_trace);
  const roadmap = record(report.personalized_skill_roadmap);
  const weekly = record(report.weekly_plan) as Record<string, string[]>;
  const readiness = record(report.readiness_scores);
  const advice = record(report.mentor_advice);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Primary Path</p>
          <h2 className="text-3xl font-bold">{payload.primary_career_path}</h2>
        </div>
        <ReportDownload report={payload} />
      </div>
      <Card className="border-primary/30 bg-primary/5">
        <CardHeader>
          <CardTitle>Executive Summary</CardTitle>
          <CardDescription>{String(executive.one_paragraph_summary || "No summary available.")}</CardDescription>
        </CardHeader>
      </Card>
      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Career Recommendation</CardTitle>
            <CardDescription>{String(career.why_this_path_fits || "-")}</CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Reasoning Trace</CardTitle>
            <CardDescription>{String(trace.why_direction_changed || trace.confidence_explanation || "-")}</CardDescription>
          </CardHeader>
        </Card>
      </div>
      <div className="grid gap-5 lg:grid-cols-[1.25fr_.75fr]">
        <CareerMatrix matrix={(report.career_fit_matrix as Array<Record<string, unknown>>) || []} />
        <Card>
          <CardHeader>
            <CardTitle>Readiness Scores</CardTitle>
            <CardDescription>Academic, clarity, internship, placement, and project readiness.</CardDescription>
          </CardHeader>
          <ReadinessScoreChart scores={readiness} />
        </Card>
      </div>
      <SkillRoadmap roadmap={roadmap} />
      <WeeklyPlan plan={weekly} />
      <ProjectCards projects={(report.project_recommendations as Array<Record<string, unknown>>) || []} />
      <Card>
        <CardHeader>
          <CardTitle>Mentor Advice</CardTitle>
          <CardDescription>{String(advice.short_advice || "-")} {String(advice.hard_truth || "")}</CardDescription>
        </CardHeader>
      </Card>
      <details className="rounded-2xl border border-border bg-card p-4">
        <summary className="cursor-pointer font-semibold">Developer JSON</summary>
        <pre className="mt-4 max-h-96 overflow-auto rounded-xl bg-background p-4 text-xs">{JSON.stringify(payload, null, 2)}</pre>
      </details>
    </div>
  );
};
