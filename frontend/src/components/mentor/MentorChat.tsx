import type { MentorAnswer } from "@/lib/types";

export const MentorChat = ({ answers }: { answers: MentorAnswer[] }) => (
  <div className="space-y-3">
    {answers.map((answer) => (
      <div key={`${answer.question_number}-${answer.question_text}`} className="rounded-2xl border border-border bg-card/70 p-4">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-primary">Q{answer.question_number}</p>
        <p className="mt-2 font-medium">{answer.question_text}</p>
        <p className="mt-3 rounded-xl bg-background/70 p-3 text-sm text-muted-foreground">{answer.answer_text}</p>
      </div>
    ))}
  </div>
);
