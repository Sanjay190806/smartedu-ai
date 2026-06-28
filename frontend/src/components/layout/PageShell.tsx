import { motion } from "framer-motion";
import type { ReactNode } from "react";

export const PageShell = ({ title, description, children }: { title: string; description: string; children: ReactNode }) => (
  <motion.main
    className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-8"
    initial={{ opacity: 0, y: 14 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.32, ease: "easeOut" }}
  >
    <div className="relative mb-6 overflow-hidden rounded-[2rem] border border-border bg-card/70 p-5 shadow-xl shadow-slate-950/5 backdrop-blur-xl dark:bg-slate-950/50">
      <div className="mesh-glow left-10 top-0 h-28 w-28 bg-primary/30" />
      <div className="mesh-glow right-8 top-4 h-28 w-28 bg-accent-violet/20" />
      <div className="relative">
        <p className="section-eyebrow">SmartEdu AI</p>
        <h2 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">{title}</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-muted-foreground md:text-base">{description}</p>
      </div>
    </div>
    {children}
  </motion.main>
);
