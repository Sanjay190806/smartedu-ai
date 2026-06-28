import { Navbar } from "@/components/layout/Navbar";
import { Card } from "@/components/ui/card";

export const AboutPage = () => (
  <div className="app-bg min-h-screen pt-24">
    <Navbar />
    <main className="mx-auto max-w-4xl px-4 py-12">
      <Card>
        <h1 className="text-3xl font-bold">About SmartEdu AI</h1>
        <p className="mt-4 leading-7 text-muted-foreground">
          SmartEdu AI combines a Python ML risk model, FastAPI persistence, explainable recommendations, and an adaptive AI mentor engine.
          The React frontend is designed as a production-grade command center for prediction, analytics, career reports, and student guidance.
        </p>
      </Card>
    </main>
  </div>
);
