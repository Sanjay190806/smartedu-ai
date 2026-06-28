import { AlertTriangle, Terminal } from "lucide-react";

import { Card } from "@/components/ui/card";

export const ErrorState = ({ title = "Something went wrong", message }: { title?: string; message: string }) => (
  <Card className="border-danger/30 bg-danger/5">
    <div className="flex gap-3">
      <AlertTriangle className="mt-1 h-5 w-5 text-danger" />
      <div>
        <h3 className="font-semibold text-danger">{title}</h3>
        <p className="mt-1 text-sm text-muted-foreground">{message}</p>
        {message.toLowerCase().includes("backend") ? (
          <div className="mt-3 flex items-center rounded-xl bg-background p-3 font-mono text-xs text-muted-foreground">
            <Terminal className="mr-2 h-4 w-4" />
            uvicorn backend.main:app --reload
          </div>
        ) : null}
      </div>
    </div>
  </Card>
);
