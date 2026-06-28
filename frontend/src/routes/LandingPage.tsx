import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { BarChart3, BrainCircuit, CheckCircle2, FileText, LineChart, Map, ShieldCheck, Sparkles, Upload, Users } from "lucide-react";

import { FeatureCard } from "@/components/cards/FeatureCard";
import { Navbar } from "@/components/layout/Navbar";
import { Button } from "@/components/ui/button";

const features = [
  ["Academic Risk Prediction", "Predict low, medium, or high academic risk from local FastAPI model artifacts.", ShieldCheck],
  ["Explainable AI", "Surface the top factors behind each prediction for mentor review.", Sparkles],
  ["AI Mentor Interview", "Adaptive question flow that turns student interests into guidance.", BrainCircuit],
  ["Career Path Recommendation", "Compare paths with confidence and reasoning trace.", Map],
  ["Skill Roadmap", "30/60/90 day and one-year plans for practical execution.", LineChart],
  ["Weekly Plan", "Daily and weekly routines grounded in academic context.", CheckCircle2],
  ["Project Suggestions", "Portfolio-ready project cards for GitHub and interviews.", FileText],
  ["Mentor Dashboard", "Analytics workspace for students, reports, and system status.", Users],
] as const;

export const LandingPage = () => (
  <div className="app-bg min-h-screen overflow-hidden">
    <Navbar />
    <main className="relative pt-24">
      <div className="aurora" />
      <section className="relative mx-auto grid max-w-7xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[1.05fr_.95fr] lg:px-8 lg:py-24">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <p className="inline-flex rounded-full border border-primary/30 bg-primary/10 px-4 py-1 text-sm font-semibold text-primary">
            AI-powered academic intelligence
          </p>
          <h1 className="mt-6 max-w-4xl text-5xl font-bold tracking-tight md:text-7xl">SmartEdu AI</h1>
          <p className="mt-6 max-w-2xl text-xl leading-8 text-muted-foreground">
            AI-powered academic risk prediction and personalized career mentoring for students.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild size="lg"><Link to="/login">Get Started</Link></Button>
            <Button asChild variant="secondary" size="lg"><Link to="/login">Try Demo</Link></Button>
            <Button asChild variant="ghost" size="lg"><a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">View API Docs</a></Button>
          </div>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.7 }} className="glass-card rounded-[2rem] p-5">
          <div className="grid gap-4">
            <div className="rounded-2xl border border-border bg-background/60 p-4">
              <p className="text-sm text-muted-foreground">Risk Prediction</p>
              <div className="mt-3 grid grid-cols-3 gap-2">
                {["Low", "Medium", "High"].map((item, index) => <div key={item} className="rounded-xl bg-primary/10 p-3 text-center text-sm font-semibold">{item}<br /><span className="text-2xl">{[68, 21, 11][index]}%</span></div>)}
              </div>
            </div>
            <div className="rounded-2xl border border-border bg-background/60 p-4">
              <p className="text-sm text-muted-foreground">AI Mentor Preview</p>
              <p className="mt-3 rounded-xl bg-primary/10 p-3 text-sm">When you work with data, do you enjoy cleaning datasets, finding insights, building ML models, or creating dashboards more?</p>
            </div>
            <div className="rounded-2xl border border-border bg-background/60 p-4">
              <p className="text-sm text-muted-foreground">Career Roadmap</p>
              <div className="mt-3 flex items-center gap-2 text-sm"><span className="rounded-full bg-success/20 px-3 py-1 text-success">Python</span><span>→</span><span className="rounded-full bg-primary/20 px-3 py-1 text-primary">SQL</span><span>→</span><span className="rounded-full bg-warning/20 px-3 py-1 text-warning">Portfolio</span></div>
            </div>
          </div>
        </motion.div>
      </section>
      <section className="relative mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-5 md:grid-cols-3">
          <div className="glass-card rounded-2xl p-6 md:col-span-2">
            <h2 className="text-2xl font-bold">Guidance usually arrives too late.</h2>
            <p className="mt-3 text-muted-foreground">SmartEdu AI identifies academic risk early, explains why a student may be struggling, and turns the next step into a mentor-ready action plan.</p>
          </div>
          <div className="glass-card rounded-2xl p-6">
            <BarChart3 className="h-8 w-8 text-primary" />
            <p className="mt-3 font-semibold">Student Data → Risk Prediction → Explainable AI → Adaptive Mentor → Career Report → Skill Roadmap</p>
          </div>
        </div>
      </section>
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {features.map(([title, description, Icon]) => <FeatureCard key={title} title={title} description={description} icon={Icon} />)}
        </div>
      </section>
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="glass-card rounded-[2rem] p-8 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-primary">Tech credibility</p>
          <p className="mt-3 text-lg text-muted-foreground">FastAPI · React · TypeScript · Tailwind · ML · Recharts · OpenRouter/Groq optional · SQLite local</p>
          <Button asChild className="mt-6" size="lg"><Link to="/login">Start SmartEdu AI</Link></Button>
        </div>
      </section>
    </main>
  </div>
);
