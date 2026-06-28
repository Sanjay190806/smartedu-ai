import { useQuery } from "@tanstack/react-query";

import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { SubjectPerformanceChart } from "@/components/charts/SubjectPerformanceChart";
import { MetricCard } from "@/components/cards/MetricCard";
import { PageShell } from "@/components/layout/PageShell";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";

export const AnalyticsPage = () => {
  const summary = useQuery({ queryKey: ["analytics-summary"], queryFn: api.getAnalyticsSummary });
  const distribution = useQuery({ queryKey: ["risk-distribution"], queryFn: api.getRiskDistribution });
  const subjects = useQuery({ queryKey: ["subject-performance"], queryFn: api.getSubjectPerformance });
  const summaryData = summary.data;
  return (
    <PageShell title="Analytics" description="Academic trends, risk distribution, and weak-subject intervention priorities.">
      {summary.isLoading ? <LoadingState /> : summary.isError ? <ErrorState message={(summary.error as Error).message} /> : summaryData ? (
        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-3">
            <MetricCard label="Average GPA" value={gpa(summaryData.average_gpa)} />
            <MetricCard label="Average Attendance" value={percent(summaryData.average_attendance)} />
            <MetricCard label="Assignment Completion" value={percent(summaryData.average_assignment_completion)} />
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            <Card><CardHeader><CardTitle>Risk Distribution</CardTitle></CardHeader><RiskDistributionChart distribution={distribution.data || {}} /></Card>
            <Card><CardHeader><CardTitle>Subject Performance</CardTitle></CardHeader><SubjectPerformanceChart subjects={subjects.data || {}} /></Card>
          </div>
        </div>
      ) : <ErrorState message="Analytics summary is unavailable." />}
    </PageShell>
  );
};
