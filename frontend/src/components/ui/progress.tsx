import { cn } from "@/lib/utils";

interface ProgressProps {
  value: number;
  className?: string;
}

export const Progress = ({ value, className }: ProgressProps) => (
  <div className={cn("h-2.5 overflow-hidden rounded-full bg-muted shadow-inner", className)}>
    <div
      className="h-full rounded-full bg-gradient-to-r from-primary via-accent-cyan to-accent-violet transition-all duration-500"
      style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
    />
  </div>
);
