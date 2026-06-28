import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Upload } from "lucide-react";

import { ErrorState } from "@/components/common/ErrorState";
import { RiskDistributionChart } from "@/components/charts/RiskDistributionChart";
import { PageShell } from "@/components/layout/PageShell";
import { RiskBadge } from "@/components/cards/RiskBadge";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import type { RiskLabel } from "@/lib/types";

export const BatchPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({ mutationFn: api.batchPredict });
  return (
    <PageShell title="Batch Upload" description="Upload a CSV matching the SmartEdu schema and run predictions in batch.">
      <div className="space-y-5">
        <Card className="border-dashed">
          <CardHeader><CardTitle>CSV Upload</CardTitle></CardHeader>
          <div className="flex flex-wrap items-center gap-3">
            <input type="file" accept=".csv" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            <Button disabled={!file || mutation.isPending} onClick={() => file && mutation.mutate(file)}>
              <Upload className="h-4 w-4" /> {mutation.isPending ? "Running..." : "Run Batch Prediction"}
            </Button>
          </div>
          <p className="mt-3 text-sm text-muted-foreground">Use `data/sample_students.csv` for a demo. The backend performs validation and prediction.</p>
        </Card>
        {mutation.isError ? <ErrorState message={(mutation.error as Error).message} /> : null}
        {mutation.data ? (
          <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]">
            <Card>
              <CardHeader><CardTitle>Risk Distribution</CardTitle></CardHeader>
              <RiskDistributionChart distribution={mutation.data.risk_distribution} type="pie" />
            </Card>
            <Card>
              <CardHeader><CardTitle>Predictions</CardTitle></CardHeader>
              <div className="max-h-96 overflow-auto">
                <table className="w-full text-left text-sm">
                  <thead className="text-muted-foreground"><tr><th className="p-3">Student</th><th>Risk</th><th>Confidence</th></tr></thead>
                  <tbody>
                    {mutation.data.predictions.map((prediction) => (
                      <tr key={prediction.student_id} className="border-t border-border">
                        <td className="p-3">{prediction.student_id}</td>
                        <td><RiskBadge risk={prediction.risk_category as RiskLabel} /></td>
                        <td>{prediction.confidence}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>
        ) : null}
      </div>
    </PageShell>
  );
};
