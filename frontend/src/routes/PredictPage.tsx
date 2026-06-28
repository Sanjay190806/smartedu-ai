import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { ErrorState } from "@/components/common/ErrorState";
import { PageShell } from "@/components/layout/PageShell";
import { PredictionForm } from "@/components/prediction/PredictionForm";
import { PredictionResult } from "@/components/prediction/PredictionResult";
import { SampleProfiles } from "@/components/prediction/SampleProfiles";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";

export const PredictPage = () => {
  const [payload, setPayload] = useState<PredictionRequest>(sampleProfiles.medium);
  const mutation = useMutation({ mutationFn: api.predictStudent });
  return (
    <PageShell title="Risk Prediction" description="Run the saved Python ML model through FastAPI and receive explainable guidance.">
      <div className="space-y-5">
        <SampleProfiles onSelect={setPayload} />
        <Card>
          <CardHeader><CardTitle>Prediction Form</CardTitle></CardHeader>
          <PredictionForm key={payload.student_id} value={payload} onChange={setPayload} onSubmit={(data) => mutation.mutate(data)} loading={mutation.isPending} />
        </Card>
        {mutation.isError ? <ErrorState message={(mutation.error as Error).message} /> : null}
        {mutation.data ? <PredictionResult result={mutation.data} /> : null}
      </div>
    </PageShell>
  );
};
