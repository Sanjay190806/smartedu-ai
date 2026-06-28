import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  ClipboardCheck,
  GraduationCap,
  ShieldAlert,
  Target,
  Users,
  Workflow,
} from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { MetricCard } from "@/components/cards/MetricCard";
import { RiskBadge } from "@/components/cards/RiskBadge";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";

const pipeline = ["Data", "Risk", "Explain", "Mentor", "Report"];

export const OverviewPage = () => {
  const summary = useQuery({ queryKey: ["analytics-summary"], queryFn: api.getAnalyticsSummary });
  const distribution = useQuery({ queryKey: ["risk-distribution"], queryFn: api.getRiskDistribution });
  const students = useQuery({ queryKey: ["students"], queryFn: api.getStudents });
  const sessions = useQuery({ queryKey: ["mentor-sessions"], queryFn: api.listMentorSessions });
  const summaryData = summary.data;
  const highRisk = summaryData?.high_risk_count || 0;
  const total = summaryData?.total_students || 0;
  const highRiskPercent = total ? (highRisk / total) * 100 : 0;

  return (
    <PageShell title="Executive Overview" description="Live academic intelligence from the FastAPI backend, shaped for mentor decisions.">
      {summary.isLoading ? <LoadingState /> : summary.isError ? <ErrorState message={(summary.error as Error).message} /> : summaryData ? (
        <div className="space-y-5">
          <section className="grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
            <Card className="relative overflow-hidden border-primary/20 bg-gradient-to-br from-primary/10 via-accent-violet/10 to-transparent">
              <div className="mesh-glow right-8 top-4 h-24 w-24 bg-primary/30" />
              <div className="relative">
                <p className="section-eyebrow">Academic intelligence workspace</p>
                <h3 className="mt-3 text-3xl font-bold tracking-tight">Catch risk early and route students to the right intervention.</h3>
                <p className="mt-3 max-w-2xl leading-7 text-muted-foreground">
                  SmartEdu AI combines risk scoring, explainability, mentor interviews, and career reports into a single local-first workspace.
                </p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <Button asChild><Link to="/app/mentor"><BrainCircuit className="h-4 w-4" /> Start AI Mentor</Link></Button>
                  <Button asChild variant="secondary"><Link to="/app/predict">Run Prediction <ArrowRight className="h-4 w-4" /></Link></Button>
                </div>
              </div>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Intervention Priority</CardTitle>
                <CardDescription>Immediate mentor attention based on saved records.</CardDescription>
              </CardHeader>
              <div className={highRisk ? "rounded-3xl border border-danger/25 bg-danger/10 p-5" : "rounded-3xl border border-success/25 bg-success/10 p-5"}>
                <div className="flex items-center gap-3">
                  <div className={highRisk ? "grid h-12 w-12 place-items-center rounded-2xl bg-danger/10 text-danger" : "grid h-12 w-12 place-items-center rounded-2xl bg-success/10 text-success"}>
                    {highRisk ? <ShieldAlert className="h-6 w-6" /> : <CheckCircle2 className="h-6 w-6" />}
                  </div>
                  <div>
                    <p className="text-3xl font-bold">{highRisk}</p>
                    <p className="text-sm text-muted-foreground">{highRisk ? "students need immediate mentor attention" : "No high-risk students in saved records"}</p>
                  </div>
                </div>
                <div className="metric-spark mt-5"><span style={{ width: `${Math.max(4, highRiskPercent)}%` }} /></div>
              </div>
            </Card>
          </section>

          <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
            <MetricCard label="Total Students" value={summaryData.total_students} helper="Saved profiles" icon={Users} progress={100} />
            <MetricCard label="High Risk" value={summaryData.high_risk_count} helper="Immediate intervention" icon={ShieldAlert} progress={highRiskPercent} />
            <MetricCard label="Average GPA" value={gpa(summaryData.average_gpa)} helper="Current GPA" icon={GraduationCap} progress={(summaryData.average_gpa / 10) * 100} />
            <MetricCard label="Attendance" value={percent(summaryData.average_attendance)} helper="Average attendance" icon={BookOpen} progress={summaryData.average_attendance} />
            <MetricCard label="Assignments" value={percent(summaryData.average_assignment_completion)} helper="Completion rate" icon={ClipboardCheck} progress={summaryData.average_assignment_completion} />
            <MetricCard label="Mentor Sessions" value={sessions.data?.length || 0} helper="Interview sessions" icon={BrainCircuit} progress={Math.min(100, (sessions.data?.length || 0) * 12)} />
          </section>

          <section className="grid gap-5 lg:grid-cols-[1.15fr_.85fr]">
            <Card>
              <CardHeader>
                <CardTitle>Risk Distribution</CardTitle>
                <CardDescription>Saved student profiles by model risk category.</CardDescription>
              </CardHeader>
              <RiskDistributionChart distribution={distribution.data || {}} />
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Weak Subject Insights</CardTitle>
                <CardDescription>Subjects that deserve mentoring, peer support, or lab reinforcement.</CardDescription>
              </CardHeader>
              <div className="grid gap-3">
                {summaryData.top_weak_subjects.length ? summaryData.top_weak_subjects.map((subject, index) => (
                  <div key={subject} className="flex items-center justify-between rounded-2xl border border-border bg-background/60 p-4">
                    <div className="flex items-center gap-3">
                      <span className="grid h-9 w-9 place-items-center rounded-xl bg-warning/10 text-sm font-bold text-warning">{index + 1}</span>
                      <div>
                        <p className="font-semibold">{subject}</p>
                        <p className="text-xs text-muted-foreground">Candidate for targeted intervention</p>
                      </div>
                    </div>
                    <Target className="h-4 w-4 text-primary" />
                  </div>
                )) : (
                  <div className="rounded-2xl border border-success/20 bg-success/10 p-4 text-sm text-success">No weak subject signals found.</div>
                )}
              </div>
            </Card>
          </section>

          <section className="grid gap-5 lg:grid-cols-[1fr_.7fr]">
            <Card>
              <CardHeader>
                <CardTitle>Recent Students</CardTitle>
                <CardDescription>Latest local records available to inspect or route into prediction.</CardDescription>
              </CardHeader>
              <div className="overflow-auto">
                <table className="data-table">
                  <thead><tr><th>Student</th><th>Department</th><th>GPA</th><th>Attendance</th><th>Action</th></tr></thead>
                  <tbody>
                    {(students.data || []).slice(0, 6).map((student) => (
                      <tr key={student.student_id}>
                        <td>
                          <p className="font-semibold">{student.name}</p>
                          <p className="text-xs text-muted-foreground">{student.student_id}</p>
                        </td>
                        <td>{student.department}</td>
                        <td>{gpa(student.latest_academic_record?.current_gpa)}</td>
                        <td>{percent(student.latest_academic_record?.attendance_percentage)}</td>
                        <td><Button asChild size="sm" variant="secondary"><Link to="/app/students">Open</Link></Button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2"><Workflow className="h-5 w-5 text-primary" /> Operating Flow</CardTitle>
                <CardDescription>How a mentor moves from data to guidance.</CardDescription>
              </CardHeader>
              <div className="space-y-3">
                {pipeline.map((step, index) => (
                  <div key={step} className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 p-3">
                    <span className="grid h-8 w-8 place-items-center rounded-full bg-primary/10 text-xs font-bold text-primary">{index + 1}</span>
                    <p className="font-medium">{step}</p>
                    {step === "Risk" ? <RiskBadge risk="High Risk" /> : null}
                  </div>
                ))}
              </div>
            </Card>
          </section>
        </div>
      ) : <ErrorState message="Analytics summary is unavailable." />}
    </PageShell>
  );
};
