import { useEffect } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "@/components/layout/ProtectedRoute";
import { AboutPage } from "@/routes/AboutPage";
import { AnalyticsPage } from "@/routes/AnalyticsPage";
import { AppShell } from "@/routes/AppShell";
import { BatchPage } from "@/routes/BatchPage";
import { LandingPage } from "@/routes/LandingPage";
import { LoginPage } from "@/routes/LoginPage";
import { MentorPage } from "@/routes/MentorPage";
import { OverviewPage } from "@/routes/OverviewPage";
import { PredictPage } from "@/routes/PredictPage";
import { PrivacyPage } from "@/routes/PrivacyPage";
import { ReportPage } from "@/routes/ReportPage";
import { SettingsPage } from "@/routes/SettingsPage";
import { StudentsPage } from "@/routes/StudentsPage";
import { SystemPage } from "@/routes/SystemPage";
import { useAppStore } from "@/store/appStore";

function App() {
  const theme = useAppStore((state) => state.theme);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    document.documentElement.classList.toggle("light", theme === "light");
  }, [theme]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/app" element={<AppShell />}>
            <Route index element={<Navigate to="/app/overview" replace />} />
            <Route path="overview" element={<OverviewPage />} />
            <Route path="predict" element={<PredictPage />} />
            <Route path="students" element={<StudentsPage />} />
            <Route path="batch" element={<BatchPage />} />
            <Route path="mentor" element={<MentorPage />} />
            <Route path="report/:sessionId" element={<ReportPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="system" element={<SystemPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
