import { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { BrainCircuit, Send } from "lucide-react";

import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { MentorChat } from "@/components/mentor/MentorChat";
import { MentorQuestionCard } from "@/components/mentor/MentorQuestionCard";
import { MetricCard } from "@/components/cards/MetricCard";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import type { MentorSession } from "@/lib/types";
import { useMentorStore } from "@/store/mentorStore";

export const MentorPage = () => {
  const [session, setSession] = useState<MentorSession | null>(null);
  const [answer, setAnswer] = useState("");
  const [studentId, setStudentId] = useState("FRONTEND_MENTOR_001");
  const [studentName, setStudentName] = useState("Demo Student");
  const provider = useQuery({ queryKey: ["provider-status"], queryFn: api.getMentorProviderStatus });
  const { setActiveSession, setActiveReport } = useMentorStore();

  const start = useMutation({
    mutationFn: api.startMentorSession,
    onSuccess: (data) => {
      setSession(data);
      setActiveSession(data);
      setActiveReport(null);
    },
  });
  const submit = useMutation({
    mutationFn: ({ id, text }: { id: string; text: string }) => api.submitMentorAnswer(id, text),
    onSuccess: async (_data, vars) => {
      const refreshed = await api.getMentorSession(vars.id);
      setSession(refreshed);
      setActiveSession(refreshed);
      setAnswer("");
    },
  });
  const report = useMutation({
    mutationFn: api.generateMentorReport,
    onSuccess: (data) => setActiveReport(data),
  });

  const progress = session ? (session.answers.length / session.max_questions) * 100 : 0;
  const ready = session ? session.status === "ready_for_report" || session.answers.length >= 8 || session.clarity_score >= 0.75 : false;
  const providerData = provider.data;

  return (
    <PageShell title="AI Mentor" description="Adaptive interview workspace with provider status, detected direction, and report generation.">
      <div className="grid gap-5 xl:grid-cols-[.85fr_1.4fr_.75fr]">
        <Card>
          <CardHeader><CardTitle>Session Setup</CardTitle></CardHeader>
          {provider.isLoading ? <LoadingState /> : provider.isError ? <ErrorState message={(provider.error as Error).message} /> : providerData ? (
            <div className="mb-5 rounded-2xl border border-border bg-background/60 p-4">
              <p className="text-sm font-semibold">Provider: {providerData.provider}</p>
              <p className="mt-1 text-sm text-muted-foreground">{providerData.provider_warning || (providerData.real_ai_configured ? "Real AI provider configured." : "Offline mentor engine active. Add OpenRouter/Groq key for deeper AI reports.")}</p>
              <p className="mt-1 text-xs text-muted-foreground">Model: {providerData.active_model}</p>
            </div>
          ) : <ErrorState message="Provider status is unavailable." />}
          <div className="space-y-3">
            <Input value={studentId} onChange={(event) => setStudentId(event.target.value)} placeholder="Student ID" />
            <Input value={studentName} onChange={(event) => setStudentName(event.target.value)} placeholder="Student name" />
            <Button
              className="w-full"
              disabled={start.isPending}
              onClick={() => start.mutate({
                student_id: studentId,
                student_name: studentName,
                academic_context: { department: "Computer Science", risk_category: "Unknown" },
                max_questions: 12,
              })}
            >
              <BrainCircuit className="h-4 w-4" /> {start.isPending ? "Starting..." : "Start Interview"}
            </Button>
          </div>
          {start.isError ? <div className="mt-4"><ErrorState message={(start.error as Error).message} /></div> : null}
        </Card>

        <Card>
          <CardHeader><CardTitle>Conversation</CardTitle></CardHeader>
          {!session ? <EmptyState title="No session yet" message="Start an interview to receive the first adaptive mentor question." /> : (
            <div className="space-y-5">
              <MentorQuestionCard session={session} />
              <Textarea value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Answer the current question..." />
              <Button disabled={!answer.trim() || submit.isPending} onClick={() => submit.mutate({ id: session.session_id, text: answer })}>
                <Send className="h-4 w-4" /> {submit.isPending ? "Submitting..." : "Submit Answer"}
              </Button>
              {submit.isError ? <ErrorState message={(submit.error as Error).message} /> : null}
              <MentorChat answers={session.answers} />
            </div>
          )}
        </Card>

        <Card>
          <CardHeader><CardTitle>Signals</CardTitle></CardHeader>
          {session ? (
            <div className="space-y-4">
              <MetricCard label="Direction" value={session.dominant_interest_area || "Exploring"} />
              <MetricCard label="Clarity" value={session.clarity_score.toFixed(2)} />
              <div>
                <div className="mb-2 flex justify-between text-sm"><span>Progress</span><span>{session.answers.length}/{session.max_questions}</span></div>
                <Progress value={progress} />
              </div>
              <Button className="w-full" disabled={!ready || report.isPending} onClick={() => report.mutate(session.session_id)}>
                Generate Report
              </Button>
              {report.data ? <Button asChild variant="secondary" className="w-full"><Link to={`/app/report/${report.data.session_id}`}>Open Report</Link></Button> : null}
              {!ready ? <p className="text-sm text-muted-foreground">Answer at least 8 questions or reach clarity 0.75 to unlock the report.</p> : null}
            </div>
          ) : <EmptyState title="Waiting for interview" message="Progress and direction appear after the first answer." />}
        </Card>
      </div>
    </PageShell>
  );
};
