import { useQuery } from "@tanstack/react-query";
import { Link, useLocation } from "react-router-dom";
import { Activity, LogOut, Menu, Sparkles } from "lucide-react";

import { ThemeToggle } from "@/components/common/ThemeToggle";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";

const routeMeta: Record<string, { title: string; subtitle: string }> = {
  "/app/overview": { title: "Executive Overview", subtitle: "Live student intelligence" },
  "/app/predict": { title: "Risk Prediction", subtitle: "ML inference workflow" },
  "/app/students": { title: "Student Records", subtitle: "Local academic profiles" },
  "/app/batch": { title: "Batch Upload", subtitle: "CSV prediction pipeline" },
  "/app/mentor": { title: "AI Mentor", subtitle: "Adaptive interview workspace" },
  "/app/analytics": { title: "Analytics", subtitle: "Academic trends and interventions" },
  "/app/system": { title: "System Status", subtitle: "Backend and provider health" },
  "/app/settings": { title: "Settings", subtitle: "Local app preferences" },
};

export const AppHeader = () => {
  const { user, logout } = useAuthStore();
  const location = useLocation();
  const { data, isError } = useQuery({ queryKey: ["health"], queryFn: api.healthCheck });
  const online = Boolean(data) && !isError;
  const meta = location.pathname.startsWith("/app/report")
    ? { title: "Mentor Report", subtitle: "Career counseling output" }
    : routeMeta[location.pathname] || { title: "SmartEdu Workspace", subtitle: "Academic intelligence command center" };

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/70 px-4 py-3 backdrop-blur-2xl lg:px-8">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Button asChild variant="ghost" size="icon" className="lg:hidden">
            <Link to="/app/overview" aria-label="Open overview">
              <Menu className="h-5 w-5" />
            </Link>
          </Button>
          <div>
            <p className="hidden text-xs font-semibold uppercase tracking-[0.18em] text-primary sm:block">{meta.subtitle}</p>
            <h1 className="text-lg font-semibold tracking-tight sm:text-xl">{meta.title}</h1>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className={online ? "premium-pill border-success/20 bg-success/10 text-success" : "premium-pill border-danger/20 bg-danger/10 text-danger"}>
            <Activity className="h-3.5 w-3.5" /> Backend {online ? "Online" : "Offline"}
          </span>
          <ThemeToggle />
          <div className="hidden items-center gap-2 rounded-full border border-border bg-card px-3 py-1.5 md:flex">
            {user?.picture ? <img src={user.picture} alt="" className="h-7 w-7 rounded-full" /> : null}
            {!user?.picture ? <Sparkles className="h-4 w-4 text-primary" /> : null}
            <span className="max-w-36 truncate text-sm">{user?.name || "Demo"}</span>
          </div>
          <Button variant="ghost" size="icon" onClick={logout} aria-label="Logout">
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
};
