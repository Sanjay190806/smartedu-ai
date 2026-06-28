import { BrainCircuit, UserRound } from "lucide-react";

import type { MentorAnswer } from "@/lib/types";

export const MentorChat = ({ answers }: { answers: MentorAnswer[] }) => (
  <div className="space-y-4">
    {answers.map((answer) => (
      <div key={`${answer.question_number}-${answer.question_text}`} className="space-y-3">
        <div className="flex items-start gap-3">
          <div className="grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-primary/10 text-primary">
            <BrainCircuit className="h-4 w-4" />
          </div>
          <div className="max-w-[88%] rounded-3xl rounded-tl-lg border border-border bg-card/80 p-4">
            <p className="text-xs font-semibold uppercase text-primary" style={{ letterSpacing: "0.16em" }}>Q{answer.question_number}</p>
            <p className="mt-2 text-sm font-medium leading-6">{answer.question_text}</p>
          </div>
        </div>
        <div className="flex items-start justify-end gap-3">
          <div className="max-w-[88%] rounded-3xl rounded-tr-lg border border-primary/20 bg-primary/10 p-4">
            <p className="text-sm leading-6 text-muted-foreground">{answer.answer_text}</p>
          </div>
          <div className="grid h-9 w-9 shrink-0 place-items-center rounded-2xl bg-muted text-muted-foreground">
            <UserRound className="h-4 w-4" />
          </div>
        </div>
      </div>
    ))}
  </div>
);
