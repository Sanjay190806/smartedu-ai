import { BrainCircuit, Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { MentorSession } from "@/lib/types";

export const MentorQuestionCard = ({ session }: { session: MentorSession }) => (
  <Card className="relative overflow-hidden border-primary/30 bg-primary/5">
    <div className="mesh-glow right-6 top-2 h-20 w-20 bg-primary/30" />
    <div className="relative flex gap-3">
      <div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-primary/10 text-primary">
        <BrainCircuit className="h-6 w-6" />
      </div>
      <div>
        <p className="section-eyebrow">Adaptive Question</p>
        <h3 className="mt-2 text-xl font-semibold leading-8">{session.current_question}</h3>
        <p className="mt-2 flex gap-2 text-sm leading-6 text-muted-foreground">
          <Sparkles className="mt-1 h-4 w-4 shrink-0 text-primary" />
          {session.current_question_reason}
        </p>
      </div>
    </div>
  </Card>
);
