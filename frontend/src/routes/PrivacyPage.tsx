import { Navbar } from "@/components/layout/Navbar";
import { Card } from "@/components/ui/card";

export const PrivacyPage = () => (
  <div className="app-bg min-h-screen pt-24">
    <Navbar />
    <main className="mx-auto max-w-4xl px-4 py-12">
      <Card>
        <h1 className="text-3xl font-bold">Privacy and AI Disclaimer</h1>
        <p className="mt-4 leading-7 text-muted-foreground">
          SmartEdu AI is academic guidance software. Predictions are probabilistic and should be reviewed by mentors and educators.
          API keys belong in backend `.env` files only. The frontend never stores OpenRouter, Groq, or backend AI provider keys.
        </p>
      </Card>
    </main>
  </div>
);
