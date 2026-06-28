import { Loader2 } from "lucide-react";

export const LoadingState = ({ label = "Loading SmartEdu AI..." }: { label?: string }) => (
  <div className="flex min-h-40 items-center justify-center rounded-2xl border border-border bg-card/70 p-6 text-muted-foreground">
    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
    {label}
  </div>
);
