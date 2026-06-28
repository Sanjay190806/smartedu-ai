import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BarChart3, BookOpen, BrainCircuit, ClipboardCheck, GraduationCap, LineChart, ShieldAlert, Target } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { SubjectPerformanceChart } from "@/components/charts/SubjectPerformanceChart";
import { MetricCard } from "@/components/cards/MetricCard";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";

export const AnalyticsPage = () => {
  const summary = useQuery({ queryKey: ["analytics-summary"], queryFn: api.getAnalyticsSummary });
  const distribution = useQuery({ queryKey: ["risk-distribution"], queryFn: api.getRiskDistribution });
  const subjects = useQuery({ queryKey: ["subject-performance"], queryFn: api.getSubjectPerformance });
  const students = useQuery({ queryKey: ["students"], queryFn: api.getStudents });
  const summaryData = summary.data;
  const departmentCounts = Object.entries((students.data || []).reduce<Record<string, number>>((acc, student) => {
    acc[student.department] = (acc[student.department] || 0) + 1;
    return acc;
  }, {})).sort((a, b) => b[1] - a[1]).slice(0, 5);

  return (
    <PageShell title="Analytics" description="Academic trends, risk distribution, weak-subject priorities, and intervention recommendations.">
      {summary.isLoading ? <LoadingState /> : summary.isError ? <ErrorState message={(summary.error as Error).message} /> : summaryData ? (
        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
            <MetricCard label="Average GPA" value={gpa(summaryData.average_gpa)} icon={GraduationCap} progress={(summaryData.average_gpa / 10) * 100} />
            <MetricCard label="Attendance" value={percent(summaryData.average_attendance)} icon={BookOpen} progress={summaryData.average_attendance} />
            <MetricCard label="Assignments" value={percent(summaryData.average_assignment_completion)} icon={ClipboardCheck} progress={summaryData.average_assignment_completion} />
            <MetricCard label="High Risk" value={summaryData.high_risk_count} icon={ShieldAlert} progress={summaryData.total_students ? (summaryData.high_risk_count / summaryData.total_students) * 100 : 0} />
            <MetricCard label="Students" value={summaryData.total_students} icon={BarChart3} progress={100} />
          </div>

          <div className="grid gap-5 lg:grid-cols-[.95fr_1.05fr]">
            <Card>
              <CardHeader>
                <CardTitle>Risk Snapshot</CardTitle>
                <CardDescription>Current saved population by risk label. Historical trend storage is not enabled yet.</CardDescription>
              </CardHeader>
              <RiskDistributionChart distribution={distribution.data || {}} />
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Subject Performance</CardTitle>
                <CardDescription>Average subject scores used for weak-area intervention planning.</CardDescription>
              </CardHeader>
              <SubjectPerformanceChart subjects={subjects.data || {}} />
            </Card>
          </div>

          <div className="grid gap-5 lg:grid-cols-[1.05fr_.95fr]">
            <Card>
              <CardHeader>
                <CardTitle>Weak Subject Interventions</CardTitle>
                <CardDescription>Convert weak signals into mentor-ready actions.</CardDescription>
              </CardHeader>
              <div className="grid gap-3 md:grid-cols-2">
                {summaryData.top_weak_subjects.length ? summaryData.top_weak_subjects.map((subject) => (
                  <div key={subject} className="rounded-3xl border border-border bg-background/60 p-4">
                    <div className="flex items-center gap-3">
                      <div className="grid h-10 w-10 place-items-center rounded-2xl bg-warning/10 text-warning"><Target className="h-5 w-5" /></div>
                      <div>
                        <p className="font-semibold">{subject}</p>
                        <p className="text-xs text-muted-foreground">Intervention priority</p>
                      </div>
                    </div>
                    <p className="mt-3 text-sm leading-6 text-muted-foreground">Schedule a focused review, assign practice tasks, and track improvement after the next internal assessment.</p>
                  </div>
                )) : <div className="rounded-3xl border border-success/20 bg-success/10 p-4 text-sm text-success">No weak subject signals detected.</div>}
              </div>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Department Insights</CardTitle>
                <CardDescription>Distribution across saved student departments.</CardDescription>
              </CardHeader>
              <div className="space-y-3">
                {departmentCounts.length ? departmentCounts.map(([department, count]) => (
                  <div key={department} className="rounded-2xl border border-border bg-background/60 p-4">
                    <div className="flex justify-between text-sm font-semibold"><span>{department}</span><span>{count}</span></div>
                    <div className="metric-spark mt-3"><span style={{ width: `${Math.max(8, (count / Math.max(1, summaryData.total_students)) * 100)}%` }} /></div>
                  </div>
                )) : <p className="text-sm text-muted-foreground">No department records available.</p>}
              </div>
            </Card>
          </div>

          <Card className="border-primary/20 bg-primary/5">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><LineChart className="h-5 w-5 text-primary" /> Action Recommendations</CardTitle>
              <CardDescription>Suggested next actions based on the current analytics snapshot.</CardDescription>
            </CardHeader>
            <div className="grid gap-3 md:grid-cols-3">
              <Button asChild><Link to="/app/predict"><ShieldAlert className="h-4 w-4" /> Run focused prediction</Link></Button>
              <Button asChild variant="secondary"><Link to="/app/mentor"><BrainCircuit className="h-4 w-4" /> Start mentor interview</Link></Button>
              <Button asChild variant="secondary"><Link to="/app/batch"><ClipboardCheck className="h-4 w-4" /> Batch review CSV</Link></Button>
            </div>
          </Card>
        </div>
      ) : <ErrorState message="Analytics summary is unavailable." />}
    </PageShell>
  );
};
