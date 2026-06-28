import { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { BrainCircuit, CheckCircle2, Compass, MessageSquare, Radio, Send, Sparkles, Target } from "lucide-react";

import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { MentorChat } from "@/components/mentor/MentorChat";
import { MentorQuestionCard } from "@/components/mentor/MentorQuestionCard";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import type { MentorSession } from "@/lib/types";
import { useMentorStore } from "@/store/mentorStore";

const signalChips = (session: MentorSession | null) => {
  if (!session) return [];
  const chips = new Set<string>();
  session.answers.forEach((answer) => {
    Object.entries(answer.detected_signals || {}).forEach(([key, value]) => {
      if (Array.isArray(value)) value.slice(0, 2).forEach((item) => chips.add(String(item)));
      else if (typeof value === "string" && value) chips.add(value);
      else chips.add(key.replace(/_/g, " "));
    });
  });
  if (session.dominant_interest_area) chips.add(session.dominant_interest_area);
  return Array.from(chips).slice(0, 8);
};

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
  const chips = signalChips(session);

  return (
    <PageShell title="AI Mentor" description="Adaptive interview workspace with provider status, detected direction, and report generation.">
      <div className="grid gap-5 xl:grid-cols-[.86fr_1.38fr_.76fr]">
        <aside className="space-y-5 xl:sticky xl:top-24 xl:self-start">
          <Card>
            <CardHeader>
              <CardTitle>Session Setup</CardTitle>
              <CardDescription>Start an adaptive interview for a student and let the mentor engine discover direction.</CardDescription>
            </CardHeader>
            {provider.isLoading ? <LoadingState /> : provider.isError ? <ErrorState message={(provider.error as Error).message} /> : providerData ? (
              <div className="mb-5 rounded-3xl border border-border bg-background/60 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <div className={providerData.real_ai_configured ? "grid h-10 w-10 place-items-center rounded-2xl bg-success/10 text-success" : "grid h-10 w-10 place-items-center rounded-2xl bg-warning/10 text-warning"}>
                      <Radio className="h-5 w-5" />
                    </div>
                    <div>
                      <p className="font-semibold">{providerData.provider}</p>
                      <p className="text-xs text-muted-foreground">{providerData.active_model}</p>
                    </div>
                  </div>
                  <span className={providerData.real_ai_configured ? "premium-pill border-success/20 bg-success/10 text-success" : "premium-pill border-warning/20 bg-warning/10 text-warning"}>
                    {providerData.real_ai_configured ? "AI" : "Fallback"}
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  {providerData.provider_warning || (providerData.real_ai_configured ? "Real AI provider configured." : "Offline mentor engine active. Add OpenRouter/Groq key for deeper AI reports.")}
                </p>
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
            <CardHeader>
              <CardTitle>Progress Timeline</CardTitle>
              <CardDescription>Reports unlock after enough signal or clarity.</CardDescription>
            </CardHeader>
            <div className="space-y-4">
              {["Identity", "Interests", "Skills", "Direction", "Report"].map((step, index) => {
                const active = session ? progress >= index * 22 : index === 0;
                return (
                  <div key={step} className="flex items-center gap-3">
                    <span className={active ? "grid h-8 w-8 place-items-center rounded-full bg-primary text-primary-foreground text-xs font-bold" : "grid h-8 w-8 place-items-center rounded-full bg-muted text-xs font-bold text-muted-foreground"}>{index + 1}</span>
                    <p className={active ? "text-sm font-semibold" : "text-sm text-muted-foreground"}>{step}</p>
                  </div>
                );
              })}
            </div>
          </Card>
        </aside>

        <Card className="min-h-[42rem]">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><MessageSquare className="h-5 w-5 text-primary" /> AI Interview Chat</CardTitle>
            <CardDescription>Answer naturally. The engine adapts follow-up questions based on detected signals.</CardDescription>
          </CardHeader>
          {!session ? (
            <EmptyState title="Start an adaptive interview" message="Start an adaptive interview to discover your best-fit academic and career path." />
          ) : (
            <div className="space-y-5">
              <MentorQuestionCard session={session} />
              <Textarea value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Answer the current question with interests, strengths, concerns, or examples..." />
              <div className="flex flex-wrap items-center justify-between gap-3">
                <p className="text-sm text-muted-foreground">Question {session.answers.length + 1} of {session.max_questions}</p>
                <Button disabled={!answer.trim() || submit.isPending} onClick={() => submit.mutate({ id: session.session_id, text: answer })}>
                  <Send className="h-4 w-4" /> {submit.isPending ? "Submitting..." : "Submit Answer"}
                </Button>
              </div>
              {submit.isError ? <ErrorState message={(submit.error as Error).message} /> : null}
              {session.answers.length ? <MentorChat answers={session.answers} /> : (
                <div className="rounded-3xl border border-dashed border-border bg-background/50 p-6 text-center text-sm text-muted-foreground">
                  Conversation history will appear here after the first answer.
                </div>
              )}
            </div>
          )}
        </Card>

        <aside className="space-y-5 xl:sticky xl:top-24 xl:self-start">
          <Card>
            <CardHeader>
              <CardTitle>Detected Signals</CardTitle>
              <CardDescription>Interest, clarity, and direction extracted from the interview.</CardDescription>
            </CardHeader>
            {session ? (
              <div className="space-y-4">
                <div className="rounded-3xl border border-border bg-background/60 p-4">
                  <p className="text-xs text-muted-foreground">Dominant direction</p>
                  <p className="mt-1 text-2xl font-bold">{session.dominant_interest_area || "Exploring"}</p>
                </div>
                <div>
                  <div className="mb-2 flex justify-between text-sm"><span>Interview progress</span><span>{session.answers.length}/{session.max_questions}</span></div>
                  <Progress value={progress} />
                </div>
                <div>
                  <div className="mb-2 flex justify-between text-sm"><span>Clarity score</span><span>{session.clarity_score.toFixed(2)}</span></div>
                  <Progress value={session.clarity_score * 100} />
                </div>
                <div className="flex flex-wrap gap-2">
                  {chips.length ? chips.map((chip) => <span key={chip} className="premium-pill">{chip}</span>) : <span className="text-sm text-muted-foreground">Signals appear after answers.</span>}
                </div>
              </div>
            ) : <EmptyState title="Waiting for interview" message="Progress and direction appear after the first answer." />}
          </Card>

          <Card className={ready ? "border-success/25 bg-success/10" : ""}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Compass className="h-5 w-5 text-primary" /> Report Readiness</CardTitle>
              <CardDescription>{ready ? "Enough signal is available to generate a report." : "Answer at least 8 questions or reach clarity 0.75."}</CardDescription>
            </CardHeader>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm">
                {ready ? <CheckCircle2 className="h-4 w-4 text-success" /> : <Sparkles className="h-4 w-4 text-primary" />}
                <span>{ready ? "Ready for full mentor report" : "Building interview context"}</span>
              </div>
              <Button className="w-full" disabled={!session || !ready || report.isPending} onClick={() => session && report.mutate(session.session_id)}>
                <Target className="h-4 w-4" /> {report.isPending ? "Generating..." : "Generate Full Mentor Report"}
              </Button>
              {report.data ? <Button asChild variant="secondary" className="w-full"><Link to={`/app/report/${report.data.session_id}`}>Open Report</Link></Button> : null}
              {report.isError ? <ErrorState message={(report.error as Error).message} /> : null}
            </div>
          </Card>
        </aside>
      </div>
    </PageShell>
  );
};
