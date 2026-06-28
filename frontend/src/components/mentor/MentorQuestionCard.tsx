import { BrainCircuit } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { MentorSession } from "@/lib/types";

export const MentorQuestionCard = ({ session }: { session: MentorSession }) => (
  <Card className="border-primary/30 bg-primary/5">
    <div className="flex gap-3">
      <BrainCircuit className="mt-1 h-6 w-6 text-primary" />
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary">Adaptive Question</p>
        <h3 className="mt-2 text-xl font-semibold">{session.current_question}</h3>
        <p className="mt-2 text-sm text-muted-foreground">{session.current_question_reason}</p>
      </div>
    </div>
  </Card>
);
