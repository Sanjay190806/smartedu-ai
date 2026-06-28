import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  Code2,
  Database,
  FileText,
  GraduationCap,
  LineChart,
  Map,
  Network,
  PanelTop,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";

import { FeatureCard } from "@/components/cards/FeatureCard";
import { Navbar } from "@/components/layout/Navbar";
import { Button } from "@/components/ui/button";

const trustPills = ["ML Risk Prediction", "Adaptive AI Mentor", "Local-first Backend", "Explainable Reports"];

const features = [
  ["Risk Prediction", "Predict low, medium, or high academic risk from attendance, GPA, marks, backlogs, and wellbeing signals.", ShieldCheck],
  ["Explainable AI", "Turn model output into top factors a mentor can understand before taking action.", Sparkles],
  ["AI Mentor Interview", "Run an adaptive interview that discovers interests, clarity, and best-fit academic direction.", BrainCircuit],
  ["Career Path Recommendation", "Compare career paths with confidence, reasoning, and practical next steps.", Map],
  ["Skill Roadmap", "Convert counseling into 30/60/90 day skill growth and a one-year plan.", LineChart],
  ["Project Recommendations", "Generate portfolio-grade projects with skills, deliverables, and GitHub value.", FileText],
  ["Analytics Dashboard", "Monitor risk distribution, weak subjects, and intervention priorities in one workspace.", BarChart3],
  ["Local-first FastAPI Backend", "Keep demo data, model artifacts, and API routes easy to run from a laptop.", Database],
] as const;

const workflow = ["Student Data", "ML Risk Engine", "Explainable Factors", "AI Mentor Interview", "Career Report", "Weekly Plan"];
const stack = ["React", "TypeScript", "FastAPI", "scikit-learn", "SQLite", "OpenRouter/Groq optional"];
const reportPreviewMetrics = [
  { label: "Risk", value: "High", icon: ShieldCheck },
  { label: "Confidence", value: "82%", icon: PanelTop },
  { label: "Clarity", value: "0.76", icon: BrainCircuit },
  { label: "Report", value: "Ready", icon: FileText },
];

export const LandingPage = () => (
  <div className="app-bg min-h-screen overflow-hidden">
    <Navbar />
    <main className="relative pt-20">
      <div className="aurora" />
      <section className="relative mx-auto grid max-w-7xl gap-10 px-4 py-12 sm:px-6 lg:grid-cols-[1.02fr_.98fr] lg:px-8 lg:py-20">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="flex flex-col justify-center">
          <p className="premium-pill w-fit border-primary/25 bg-primary/10 text-primary">
            <Sparkles className="h-3.5 w-3.5" /> AI academic intelligence product
          </p>
          <h1 className="mt-6 max-w-4xl text-5xl font-bold tracking-tight md:text-7xl">
            SmartEdu AI
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-muted-foreground md:text-xl">
            Explainable student performance prediction and personalized academic guidance for mentors who need to act before risk becomes failure.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild size="lg"><Link to="/login">Start Demo <ArrowRight className="h-4 w-4" /></Link></Button>
            <Button asChild variant="secondary" size="lg"><Link to="/app/overview">View Dashboard</Link></Button>
            <Button asChild variant="ghost" size="lg"><a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">API Docs</a></Button>
          </div>
          <div className="mt-8 flex flex-wrap gap-2">
            {trustPills.map((pill) => (
              <span key={pill} className="premium-pill">
                <CheckCircle2 className="h-3.5 w-3.5 text-success" /> {pill}
              </span>
            ))}
          </div>
        </motion.div>

        <motion.div
          id="product"
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7 }}
          className="hero-panel"
        >
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="section-eyebrow">Command preview</p>
              <h2 className="mt-1 text-xl font-semibold">Academic intelligence cockpit</h2>
            </div>
            <span className="premium-pill border-success/20 bg-success/10 text-success">Backend online</span>
          </div>
          <div className="grid gap-4">
            <div className="grid gap-3 md:grid-cols-3">
              {[
                ["Low", "68%", "bg-success/10 text-success"],
                ["Medium", "21%", "bg-warning/10 text-warning"],
                ["High", "11%", "bg-danger/10 text-danger"],
              ].map(([label, value, className]) => (
                <div key={label} className="rounded-2xl border border-border bg-background/60 p-4">
                  <p className="text-xs text-muted-foreground">{label} risk</p>
                  <p className="mt-2 text-3xl font-bold">{value}</p>
                  <div className="metric-spark mt-3"><span className={className} style={{ width: value }} /></div>
                </div>
              ))}
            </div>
            <div className="grid gap-4 lg:grid-cols-[1.08fr_.92fr]">
              <div className="rounded-3xl border border-border bg-background/60 p-5">
                <p className="text-sm font-semibold text-primary">AI mentor question</p>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">
                  When you work with data, do you enjoy cleaning datasets, finding patterns, building ML models, or presenting insights?
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {["ML", "Analytics", "Dashboards"].map((chip) => <span key={chip} className="premium-pill">{chip}</span>)}
                </div>
              </div>
              <div className="rounded-3xl border border-border bg-background/60 p-5">
                <p className="text-sm font-semibold text-primary">Career roadmap</p>
                <div className="mt-4 space-y-3">
                  {["Python foundations", "SQL portfolio", "ML project", "Placement story"].map((item, index) => (
                    <div key={item} className="flex items-center gap-3 text-sm">
                      <span className="grid h-7 w-7 place-items-center rounded-full bg-primary/10 text-xs font-bold text-primary">{index + 1}</span>
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="grid gap-3 md:grid-cols-4">
              {reportPreviewMetrics.map(({ label, value, icon: Icon }) => (
                <div key={label} className="rounded-2xl border border-border bg-background/60 p-4">
                  <Icon className="h-5 w-5 text-primary" />
                  <p className="mt-3 text-xs text-muted-foreground">{label}</p>
                  <p className="text-lg font-bold">{value}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      <section className="relative mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-5 lg:grid-cols-[.9fr_1.1fr]">
          <div className="glass-card rounded-[2rem] p-7">
            <p className="section-eyebrow">Problem</p>
            <h2 className="mt-3 text-3xl font-bold tracking-tight">Students often receive support too late.</h2>
            <p className="mt-4 leading-7 text-muted-foreground">
              Academic signals are scattered across attendance, marks, submissions, LMS activity, and wellbeing. By the time a mentor sees the pattern, the student may already be in high-risk territory.
            </p>
          </div>
          <div className="glass-card rounded-[2rem] p-7">
            <p className="section-eyebrow">Solution</p>
            <h2 className="mt-3 text-3xl font-bold tracking-tight">Detect risk early, explain why, then guide the next action.</h2>
            <p className="mt-4 leading-7 text-muted-foreground">
              SmartEdu AI combines a local ML risk engine with explainable factors and an adaptive AI mentor workflow to produce academic support, career direction, and weekly execution plans.
            </p>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="section-eyebrow">Capabilities</p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight">Built for academic intervention and guidance.</h2>
          </div>
          <Button asChild variant="secondary"><Link to="/login">Explore demo</Link></Button>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map(([title, description, Icon]) => <FeatureCard key={title} title={title} description={description} icon={Icon} />)}
        </div>
      </section>

      <section id="workflow" className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="glass-card rounded-[2rem] p-7">
          <div className="mb-6 flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl border border-primary/20 bg-primary/10 text-primary">
              <Workflow className="h-5 w-5" />
            </div>
            <div>
              <p className="section-eyebrow">Workflow timeline</p>
              <h2 className="text-2xl font-bold tracking-tight">From student data to mentor-ready plan</h2>
            </div>
          </div>
          <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
            {workflow.map((step, index) => (
              <div key={step} className="rounded-2xl border border-border bg-background/60 p-4">
                <span className="grid h-8 w-8 place-items-center rounded-full bg-primary/10 text-xs font-bold text-primary">{index + 1}</span>
                <p className="mt-3 text-sm font-semibold">{step}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="stack" className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
          <div className="glass-card rounded-[2rem] p-7">
            <Code2 className="h-8 w-8 text-primary" />
            <h2 className="mt-4 text-3xl font-bold tracking-tight">Modern stack, local demo friendly.</h2>
            <p className="mt-4 leading-7 text-muted-foreground">
              A portfolio-grade frontend on top of a Python ML backend, with optional AI providers kept server-side.
            </p>
          </div>
          <div className="grid gap-3 md:grid-cols-3">
            {stack.map((item) => (
              <div key={item} className="glass-card rounded-2xl p-5">
                <Network className="h-5 w-5 text-primary" />
                <p className="mt-3 font-semibold">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 pb-16 pt-8 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-[2rem] border border-primary/20 bg-gradient-to-br from-primary/20 via-accent-violet/10 to-success/10 p-8 text-center shadow-glow">
          <GraduationCap className="mx-auto h-10 w-10 text-primary" />
          <h2 className="mt-4 text-3xl font-bold tracking-tight">Turn academic risk into a guided recovery path.</h2>
          <p className="mx-auto mt-3 max-w-2xl text-muted-foreground">
            Start the demo, run a prediction, interview a student, and generate a career counseling report from the same workspace.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button asChild size="lg"><Link to="/login">Start SmartEdu AI <ArrowRight className="h-4 w-4" /></Link></Button>
            <Button asChild variant="secondary" size="lg"><Link to="/app/overview">Open Dashboard</Link></Button>
          </div>
        </div>
      </section>
    </main>
  </div>
);
