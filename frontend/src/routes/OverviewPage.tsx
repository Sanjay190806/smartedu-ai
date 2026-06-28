import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, BrainCircuit, GraduationCap, ShieldAlert, Users } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { MetricCard } from "@/components/cards/MetricCard";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";

export const OverviewPage = () => {
  const summary = useQuery({ queryKey: ["analytics-summary"], queryFn: api.getAnalyticsSummary });
  const distribution = useQuery({ queryKey: ["risk-distribution"], queryFn: api.getRiskDistribution });
  const students = useQuery({ queryKey: ["students"], queryFn: api.getStudents });
  const summaryData = summary.data;

  return (
    <PageShell title="Executive Overview" description="Live academic intelligence from the FastAPI backend.">
      {summary.isLoading ? <LoadingState /> : summary.isError ? <ErrorState message={(summary.error as Error).message} /> : summaryData ? (
        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Total Students" value={summaryData.total_students} helper="Saved profiles" icon={Users} />
            <MetricCard label="High Risk" value={summaryData.high_risk_count} helper="Immediate intervention" icon={ShieldAlert} />
            <MetricCard label="Average GPA" value={gpa(summaryData.average_gpa)} helper="Current GPA" icon={GraduationCap} />
            <MetricCard label="Attendance" value={percent(summaryData.average_attendance)} helper="Average attendance" icon={BookOpen} />
          </div>
          <div className="grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
            <Card>
              <CardHeader><CardTitle>Risk Distribution</CardTitle></CardHeader>
              <RiskDistributionChart distribution={distribution.data || {}} />
            </Card>
            <Card>
              <CardHeader><CardTitle>Weak Subject Insights</CardTitle></CardHeader>
              <div className="space-y-2">
                {summaryData.top_weak_subjects.map((subject) => <div key={subject} className="rounded-xl border border-border bg-background/60 p-3">{subject}</div>)}
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                <Button asChild><Link to="/app/mentor"><BrainCircuit className="h-4 w-4" /> Start AI Mentor</Link></Button>
                <Button asChild variant="secondary"><Link to="/app/predict">Run Prediction</Link></Button>
              </div>
            </Card>
          </div>
          <Card>
            <CardHeader><CardTitle>Recent Students</CardTitle></CardHeader>
            <div className="grid gap-3 md:grid-cols-3">
              {(students.data || []).slice(0, 6).map((student) => (
                <div key={student.student_id} className="rounded-xl border border-border bg-background/60 p-3">
                  <p className="font-semibold">{student.name}</p>
                  <p className="text-sm text-muted-foreground">{student.department} · Year {student.year}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      ) : <ErrorState message="Analytics summary is unavailable." />}
    </PageShell>
  );
};
