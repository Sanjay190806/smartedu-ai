import { NavLink } from "react-router-dom";
import {
  Activity,
  BarChart3,
  BrainCircuit,
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

const items = [
  { label: "Overview", href: "/app/overview", icon: LayoutDashboard },
  { label: "Risk Prediction", href: "/app/predict", icon: ShieldCheck },
  { label: "Students", href: "/app/students", icon: Users },
  { label: "Batch Upload", href: "/app/batch", icon: Upload },
  { label: "AI Mentor", href: "/app/mentor", icon: BrainCircuit },
  { label: "Reports", href: "/app/report/latest", icon: FileText },
  { label: "Analytics", href: "/app/analytics", icon: BarChart3 },
  { label: "System", href: "/app/system", icon: Activity },
  { label: "Settings", href: "/app/settings", icon: Settings },
];

export const Sidebar = () => (
  <aside className="hidden h-screen w-72 shrink-0 border-r border-border bg-card/40 p-4 backdrop-blur-xl lg:sticky lg:top-0 lg:block">
    <div className="mb-8 flex items-center gap-3 px-2">
      <div className="grid h-10 w-10 place-items-center rounded-2xl bg-primary text-primary-foreground">
        <GraduationCap className="h-5 w-5" />
      </div>
      <div>
        <p className="font-bold">SmartEdu AI</p>
        <p className="text-xs text-muted-foreground">Command Center</p>
      </div>
    </div>
    <nav className="space-y-1">
      {items.map((item) => (
        <NavLink
          key={item.href}
          to={item.href}
          className={({ isActive }) =>
            cn(
              "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground",
              isActive && "bg-primary/12 text-primary ring-1 ring-primary/20",
            )
          }
        >
          <item.icon className="h-4 w-4" />
          {item.label}
        </NavLink>
      ))}
    </nav>
    <div className="mt-8 rounded-2xl border border-border bg-background/60 p-4">
      <LineChart className="h-5 w-5 text-primary" />
      <p className="mt-3 text-sm font-semibold">Local-first demo</p>
      <p className="mt-1 text-xs leading-5 text-muted-foreground">Connects to FastAPI and SQLite. Streamlit remains as backup.</p>
    </div>
  </aside>
);
