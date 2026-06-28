import { Navigate, Outlet, useLocation } from "react-router-dom";

import { AppHeader } from "@/components/layout/AppHeader";
import { Sidebar } from "@/components/layout/Sidebar";

export const AppShell = () => {
  const location = useLocation();
  if (location.pathname === "/app") return <Navigate to="/app/overview" replace />;
  return (
    <div className="app-bg min-h-screen">
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="min-w-0 flex-1">
          <AppHeader />
          <Outlet />
        </div>
      </div>
    </div>
  );
};
