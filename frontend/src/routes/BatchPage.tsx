import { useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Download, FileSpreadsheet, ShieldAlert, Table2, Upload } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { MetricCard } from "@/components/cards/MetricCard";
import { RiskBadge } from "@/components/cards/RiskBadge";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import type { BatchPredictionResponse } from "@/lib/types";

const requiredColumns = ["student_id", "name", "department", "attendance_percentage", "current_gpa", "backlogs", "stress_level", "sleep_hours"];

function downloadBatch(payload: BatchPredictionResponse) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "smartedu-batch-predictions.json";
  link.click();
  URL.revokeObjectURL(url);
}

export const BatchPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({ mutationFn: api.batchPredict });
  const highRisk = useMemo(() => (mutation.data?.predictions || []).filter((prediction) => prediction.risk_category === "High Risk"), [mutation.data]);

  return (
    <PageShell title="Batch Upload" description="Upload a SmartEdu CSV and run bulk predictions through the FastAPI batch endpoint.">
      <div className="space-y-5">
        <div className="grid gap-5 lg:grid-cols-[1fr_.85fr]">
          <Card className="border-dashed border-primary/30 bg-primary/5">
            <CardHeader>
              <CardTitle>CSV Upload Zone</CardTitle>
              <CardDescription>Use `data/sample_students.csv` for a demo, or upload a schema-compatible CSV.</CardDescription>
            </CardHeader>
            <label className="block cursor-pointer rounded-[2rem] border border-dashed border-border bg-background/60 p-8 text-center transition hover:border-primary/40 hover:bg-primary/5">
              <Upload className="mx-auto h-10 w-10 text-primary" />
              <p className="mt-3 font-semibold">{file ? file.name : "Choose a CSV file"}</p>
              <p className="mt-1 text-sm text-muted-foreground">{file ? `${Math.round(file.size / 1024)} KB ready for prediction` : "Drag-style upload surface with native file picker"}</p>
              <input className="sr-only" type="file" accept=".csv" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            </label>
            <div className="mt-5 flex flex-wrap gap-3">
              <Button disabled={!file || mutation.isPending} onClick={() => file && mutation.mutate(file)}>
                <Upload className="h-4 w-4" /> {mutation.isPending ? "Running..." : "Run Batch Prediction"}
              </Button>
              {mutation.data ? (
                <Button variant="secondary" onClick={() => downloadBatch(mutation.data)}>
                  <Download className="h-4 w-4" /> Download Results
                </Button>
              ) : null}
            </div>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Schema Readiness</CardTitle>
              <CardDescription>Backend validates the full dataset; these are the most important identifiers and risk features.</CardDescription>
            </CardHeader>
            <div className="flex flex-wrap gap-2">
              {requiredColumns.map((column) => <span key={column} className="premium-pill"><FileSpreadsheet className="h-3.5 w-3.5 text-primary" /> {column}</span>)}
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-border bg-background/60 p-4">
                <p className="text-xs text-muted-foreground">Expected format</p>
                <p className="mt-1 font-semibold">CSV</p>
              </div>
              <div className="rounded-2xl border border-border bg-background/60 p-4">
                <p className="text-xs text-muted-foreground">Model output</p>
                <p className="mt-1 font-semibold">Risk + Guidance</p>
              </div>
            </div>
          </Card>
        </div>

        {mutation.isError ? <ErrorState message={(mutation.error as Error).message} /> : null}

        {mutation.data ? (
          <div className="space-y-5">
            <div className="grid gap-4 md:grid-cols-4">
              <MetricCard label="Rows Processed" value={mutation.data.total_records} helper="CSV records" icon={Table2} progress={100} />
              <MetricCard label="High Risk" value={highRisk.length} helper="Immediate attention" icon={ShieldAlert} progress={mutation.data.total_records ? (highRisk.length / mutation.data.total_records) * 100 : 0} />
              <MetricCard label="Low Risk" value={mutation.data.risk_distribution["Low Risk"] || 0} helper="Stable" icon={FileSpreadsheet} progress={mutation.data.total_records ? ((mutation.data.risk_distribution["Low Risk"] || 0) / mutation.data.total_records) * 100 : 0} />
              <MetricCard label="Medium Risk" value={mutation.data.risk_distribution["Medium Risk"] || 0} helper="Monitor" icon={ShieldAlert} progress={mutation.data.total_records ? ((mutation.data.risk_distribution["Medium Risk"] || 0) / mutation.data.total_records) * 100 : 0} />
            </div>

            <div className="grid gap-5 lg:grid-cols-[.85fr_1.15fr]">
              <Card>
                <CardHeader>
                  <CardTitle>Batch Risk Distribution</CardTitle>
                  <CardDescription>Prediction output across all uploaded rows.</CardDescription>
                </CardHeader>
                <RiskDistributionChart distribution={mutation.data.risk_distribution} type="pie" />
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Prediction Results</CardTitle>
                  <CardDescription>Scrollable result table with confidence and generated risk class.</CardDescription>
                </CardHeader>
                <div className="max-h-96 overflow-auto">
                  <table className="data-table">
                    <thead><tr><th>Student</th><th>Risk</th><th>Confidence</th><th>Top Factor</th></tr></thead>
                    <tbody>
                      {mutation.data.predictions.map((prediction) => (
                        <tr key={prediction.student_id}>
                          <td>{prediction.student_id}</td>
                          <td><RiskBadge risk={prediction.risk_category} /></td>
                          <td>{prediction.confidence}</td>
                          <td className="max-w-xs truncate">{prediction.top_factors?.[0] || "-"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>High-Risk Spotlight</CardTitle>
                <CardDescription>Students to prioritize for mentor outreach after the batch run.</CardDescription>
              </CardHeader>
              {highRisk.length ? (
                <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                  {highRisk.slice(0, 9).map((prediction) => (
                    <div key={prediction.student_id} className="rounded-3xl border border-danger/25 bg-danger/10 p-4">
                      <RiskBadge risk="High Risk" />
                      <p className="mt-3 font-semibold">{prediction.student_id}</p>
                      <p className="mt-1 text-sm text-muted-foreground">{prediction.recommendations?.summary || prediction.explanation}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="rounded-3xl border border-success/20 bg-success/10 p-5 text-sm text-success">No high-risk students in this batch result.</div>
              )}
            </Card>
          </div>
        ) : null}
      </div>
    </PageShell>
  );
};
