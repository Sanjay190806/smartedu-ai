import { NavLink } from "react-router-dom";
import {
  Activity,
  BarChart3,
  BrainCircuit,
  ChevronRight,
  CircleDot,
  FileText,
  GraduationCap,
  LayoutDashboard,
  LineChart,
  Settings,
  ShieldCheck,
  Upload,
  Users,
} from "lucide-react";

import { cn } from "@/lib/utils";

const groups = [
  {
    label: "Command",
    items: [
      { label: "Overview", href: "/app/overview", icon: LayoutDashboard },
      { label: "Risk Prediction", href: "/app/predict", icon: ShieldCheck },
      { label: "Students", href: "/app/students", icon: Users },
      { label: "Batch Upload", href: "/app/batch", icon: Upload },
    ],
  },
  {
    label: "Guidance",
    items: [
      { label: "AI Mentor", href: "/app/mentor", icon: BrainCircuit },
      { label: "Reports", href: "/app/report/latest", icon: FileText },
      { label: "Analytics", href: "/app/analytics", icon: BarChart3 },
    ],
  },
  {
    label: "Ops",
    items: [
      { label: "System", href: "/app/system", icon: Activity },
      { label: "Settings", href: "/app/settings", icon: Settings },
    ],
  },
];

export const Sidebar = () => (
  <aside className="hidden h-screen w-72 shrink-0 border-r border-border bg-card/50 p-4 backdrop-blur-2xl lg:sticky lg:top-0 lg:block">
    <div className="mb-8 flex items-center gap-3 px-2">
      <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-primary to-accent-violet text-primary-foreground shadow-lg shadow-cyan-500/20">
        <GraduationCap className="h-5 w-5" />
      </div>
      <div>
        <p className="font-bold">SmartEdu AI</p>
        <p className="text-xs text-muted-foreground">Academic OS</p>
      </div>
    </div>
    <nav className="space-y-5">
      {groups.map((group) => (
        <div key={group.label}>
          <p className="mb-2 px-3 text-[0.68rem] font-bold uppercase text-muted-foreground" style={{ letterSpacing: "0.16em" }}>{group.label}</p>
          <div className="space-y-1">
            {group.items.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    "group flex items-center justify-between rounded-2xl px-3 py-2.5 text-sm font-medium text-muted-foreground transition hover:bg-muted/80 hover:text-foreground",
                    isActive && "bg-primary/10 text-primary ring-1 ring-primary/20",
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <span className="flex items-center gap-3">
                      <item.icon className="h-4 w-4" />
                      {item.label}
                    </span>
                    {isActive ? <ChevronRight className="h-4 w-4" /> : null}
                  </>
                )}
              </NavLink>
            ))}
          </div>
        </div>
      ))}
    </nav>
    <div className="mt-8 rounded-3xl border border-border bg-background/60 p-4 shadow-inner-glow">
      <div className="flex items-center justify-between">
        <LineChart className="h-5 w-5 text-primary" />
        <span className="inline-flex items-center gap-1 rounded-full bg-success/10 px-2 py-1 text-[0.68rem] font-bold text-success">
          <CircleDot className="h-3 w-3" /> Demo
        </span>
      </div>
      <p className="mt-3 text-sm font-semibold">Local-first mode</p>
      <p className="mt-1 text-xs leading-5 text-muted-foreground">FastAPI, SQLite, ML artifacts, and optional AI provider. Streamlit backup remains untouched.</p>
    </div>
  </aside>
);
