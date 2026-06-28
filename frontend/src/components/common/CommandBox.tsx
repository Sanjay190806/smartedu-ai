import { Terminal } from "lucide-react";

export const CommandBox = ({ command }: { command: string }) => (
  <div className="flex items-center gap-2 rounded-xl border border-border bg-background p-3 font-mono text-xs text-muted-foreground">
    <Terminal className="h-4 w-4 text-primary" />
    {command}
  </div>
);
