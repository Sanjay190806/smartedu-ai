import { useQuery } from "@tanstack/react-query";
import { LogOut, Menu } from "lucide-react";

import { ThemeToggle } from "@/components/common/ThemeToggle";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";

export const AppHeader = () => {
  const { user, logout } = useAuthStore();
  const { data, isError } = useQuery({ queryKey: ["health"], queryFn: api.healthCheck });
  const online = Boolean(data) && !isError;

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/70 px-4 py-3 backdrop-blur-xl lg:px-8">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" className="lg:hidden">
            <Menu className="h-5 w-5" />
          </Button>
          <div>
            <p className="text-sm text-muted-foreground">SmartEdu AI</p>
            <h1 className="text-xl font-semibold">Academic Intelligence Workspace</h1>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className={online ? "rounded-full bg-success/10 px-3 py-1 text-xs font-semibold text-success" : "rounded-full bg-danger/10 px-3 py-1 text-xs font-semibold text-danger"}>
            Backend {online ? "Online" : "Offline"}
          </span>
          <ThemeToggle />
          <div className="hidden items-center gap-2 rounded-full border border-border bg-card px-3 py-1.5 md:flex">
            {user?.picture ? <img src={user.picture} alt="" className="h-7 w-7 rounded-full" /> : null}
            <span className="text-sm">{user?.name || "Demo"}</span>
          </div>
          <Button variant="ghost" size="icon" onClick={logout} aria-label="Logout">
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
};
