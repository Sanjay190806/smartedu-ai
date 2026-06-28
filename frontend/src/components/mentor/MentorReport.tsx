import type { LucideIcon } from "lucide-react";
import { Award, BookOpen, BrainCircuit, Briefcase, CalendarDays, CheckCircle2, Compass, Lightbulb, Target, TrendingUp } from "lucide-react";

import { CareerMatrix } from "./CareerMatrix";
import { ProjectCards } from "./ProjectCards";
import { ReportDownload } from "./ReportDownload";
import { SkillRoadmap } from "./SkillRoadmap";
import { WeeklyPlan } from "./WeeklyPlan";

import { ReadinessScoreChart } from "@/components/charts/ReadinessScoreChart";
import { Progress } from "@/components/ui/progress";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { titleCase } from "@/lib/formatters";
import type { MentorReport as MentorReportType } from "@/lib/types";

const record = (value: unknown) => (typeof value === "object" && value !== null ? (value as Record<string, unknown>) : {});
const list = (value: unknown) => (Array.isArray(value) ? value.map(String) : value ? [String(value)] : []);

const AdviceCard = ({ title, value, icon: Icon }: { title: string; value: unknown; icon: LucideIcon }) => (
  <div className="rounded-3xl border border-border bg-background/60 p-4">
    <div className="mb-3 flex items-center gap-2">
      <div className="grid h-9 w-9 place-items-center rounded-xl bg-primary/10 text-primary"><Icon className="h-4 w-4" /></div>
      <p className="font-semibold">{title}</p>
    </div>
    {Array.isArray(value) ? (
      <ul className="space-y-2 text-sm text-muted-foreground">
        {value.map((item) => <li key={String(item)} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-primary" /> {String(item)}</li>)}
      </ul>
    ) : (
      <p className="text-sm leading-6 text-muted-foreground">{String(value || "-")}</p>
    )}
  </div>
);

const SkillColumn = ({ title, values, tone }: { title: string; values: string[]; tone: string }) => (
  <div className="rounded-3xl border border-border bg-background/60 p-4">
    <p className="font-semibold">{title}</p>
    <div className="mt-3 flex flex-wrap gap-2">
      {(values.length ? values : ["Not detected yet"]).map((skill) => (
        <span key={skill} className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${tone}`}>{skill}</span>
      ))}
    </div>
  </div>
);

export const MentorReport = ({ payload }: { payload: MentorReportType }) => {
  const report = payload.report;
  const executive = record(report.executive_summary);
  const career = record(report.career_path_recommendation);
  const trace = record(report.career_reasoning_trace);
  const roadmap = record(report.personalized_skill_roadmap);
  const weekly = record(report.weekly_plan) as Record<string, string[]>;
  const readiness = record(report.readiness_scores);
  const advice = record(report.mentor_advice);
  const skillGap = record(report.skill_gap_analysis);
  const resources = record(report.resource_recommendations);
  const oneYear = record(report.one_year_growth_plan);
  const dailyPattern = report.daily_learning_pattern;
  const confidence = Math.round((payload.confidence_score <= 1 ? payload.confidence_score * 100 : payload.confidence_score) || Number(executive.confidence || 0));

  return (
    <div className="space-y-5">
      <section className="relative overflow-hidden rounded-[2rem] border border-primary/20 bg-gradient-to-br from-primary/10 via-accent-violet/10 to-transparent p-6 shadow-glow">
        <div className="mesh-glow right-8 top-4 h-28 w-28 bg-primary/30" />
        <div className="relative flex flex-wrap items-start justify-between gap-5">
          <div className="max-w-3xl">
            <p className="section-eyebrow">Career counseling report</p>
            <h2 className="mt-3 text-4xl font-bold tracking-tight">{payload.primary_career_path}</h2>
            <p className="mt-3 leading-7 text-muted-foreground">
              {String(career.why_this_path_fits || executive.one_paragraph_summary || "Personalized mentor report generated from interview signals.")}
            </p>
            <div className="mt-5 flex flex-wrap gap-2">
              <span className="premium-pill"><Award className="h-3.5 w-3.5 text-primary" /> Confidence {confidence}%</span>
              <span className="premium-pill"><BrainCircuit className="h-3.5 w-3.5 text-primary" /> Session {payload.session_id}</span>
              {payload.student_id ? <span className="premium-pill"><Compass className="h-3.5 w-3.5 text-primary" /> {payload.student_id}</span> : null}
            </div>
          </div>
          <ReportDownload report={payload} />
        </div>
      </section>

      <Card className="border-primary/20 bg-primary/5">
        <CardHeader>
          <CardTitle>Executive Summary</CardTitle>
          <CardDescription>{String(executive.one_paragraph_summary || "No summary available.")}</CardDescription>
        </CardHeader>
        <div className="grid gap-3 md:grid-cols-3">
          {[
            ["Best fit", executive.best_fit_path || payload.primary_career_path],
            ["Immediate priority", executive.immediate_priority],
            ["Next best action", executive.next_best_action],
          ].map(([label, value]) => (
            <div key={String(label)} className="rounded-2xl border border-border bg-background/60 p-4">
              <p className="text-xs text-muted-foreground">{String(label)}</p>
              <p className="mt-2 font-semibold">{String(value || "-")}</p>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-5 lg:grid-cols-[1.15fr_.85fr]">
        <CareerMatrix matrix={(report.career_fit_matrix as Array<Record<string, unknown>>) || []} />
        <Card>
          <CardHeader>
            <CardTitle>Readiness Scores</CardTitle>
            <CardDescription>Academic, career clarity, internship, placement, and project readiness.</CardDescription>
          </CardHeader>
          <ReadinessScoreChart scores={readiness} />
          <div className="mt-4 space-y-3">
            {Object.entries(readiness).map(([key, value]) => (
              <div key={key}>
                <div className="mb-1 flex justify-between text-sm"><span>{titleCase(key)}</span><span>{Number(value || 0)}%</span></div>
                <Progress value={Number(value || 0)} />
              </div>
            ))}
          </div>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Skills Strategy</CardTitle>
          <CardDescription>What the student already has, what must be built now, and what can wait.</CardDescription>
        </CardHeader>
        <div className="grid gap-4 lg:grid-cols-4">
          <SkillColumn title="Current skills" values={list(skillGap.current_known_skills)} tone="border-success/25 bg-success/10 text-success" />
          <SkillColumn title="Must build now" values={list(skillGap.skills_to_improve_first)} tone="border-danger/25 bg-danger/10 text-danger" />
          <SkillColumn title="Core gaps" values={list(skillGap.missing_core_skills)} tone="border-warning/25 bg-warning/10 text-warning" />
          <SkillColumn title="Optional later" values={list(skillGap.skills_not_needed_right_now)} tone="border-primary/25 bg-primary/10 text-primary" />
        </div>
      </Card>

      <SkillRoadmap roadmap={roadmap} />

      <Card>
        <CardHeader>
          <CardTitle>One-Year Growth Plan</CardTitle>
          <CardDescription>Longer path after the immediate 30/60/90 day roadmap.</CardDescription>
        </CardHeader>
        <div className="grid gap-3 md:grid-cols-3">
          {Object.entries(oneYear).map(([key, value]) => (
            <div key={key} className="rounded-3xl border border-border bg-background/60 p-4">
              <p className="font-semibold">{titleCase(key)}</p>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {list(value).map((item) => <li key={item} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-primary" /> {item}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Daily Learning Pattern</CardTitle>
            <CardDescription>Recommended cadence for consistent growth.</CardDescription>
          </CardHeader>
          <div className="rounded-3xl border border-border bg-background/60 p-4 text-sm leading-6 text-muted-foreground">
            {Array.isArray(dailyPattern) ? dailyPattern.join(", ") : String(dailyPattern || "Protect a consistent daily learning block and publish weekly evidence.")}
          </div>
        </Card>
        <WeeklyPlan plan={weekly} />
      </div>

      <ProjectCards projects={(report.project_recommendations as Array<Record<string, unknown>>) || []} />

      <Card>
        <CardHeader>
          <CardTitle>Resources</CardTitle>
          <CardDescription>Recommended learning and practice resources for the selected path.</CardDescription>
        </CardHeader>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {Object.entries(resources).map(([key, value]) => (
            <AdviceCard key={key} title={titleCase(key)} value={list(value)} icon={BookOpen} />
          ))}
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Mentor Advice</CardTitle>
          <CardDescription>Actionable counseling notes for the student and mentor.</CardDescription>
        </CardHeader>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <AdviceCard title="Hard truth" value={advice.hard_truth} icon={Target} />
          <AdviceCard title="Encouragement" value={advice.encouragement} icon={Lightbulb} />
          <AdviceCard title="Next best action" value={advice.next_best_action} icon={TrendingUp} />
          <AdviceCard title="Stop doing" value={advice.what_to_stop_doing} icon={Briefcase} />
          <AdviceCard title="Continue doing" value={advice.what_to_continue_doing} icon={CalendarDays} />
          <AdviceCard title="Short advice" value={advice.short_advice} icon={Compass} />
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Reasoning Trace</CardTitle>
          <CardDescription>{String(trace.why_direction_changed || trace.confidence_explanation || "The recommendation is based on interview signals and academic context.")}</CardDescription>
        </CardHeader>
      </Card>

      <details className="rounded-3xl border border-border bg-card/80 p-4">
        <summary className="cursor-pointer font-semibold">Developer JSON</summary>
        <pre className="mt-4 max-h-96 overflow-auto rounded-2xl bg-background p-4 text-xs">{JSON.stringify(payload, null, 2)}</pre>
      </details>
    </div>
  );
};
