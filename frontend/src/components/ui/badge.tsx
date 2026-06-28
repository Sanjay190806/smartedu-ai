import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
}

export const Badge = ({ children, className }: BadgeProps) => (
  <span className={cn("inline-flex items-center gap-1.5 rounded-full border border-border bg-muted/70 px-2.5 py-1 text-xs font-semibold text-muted-foreground", className)}>
    {children}
  </span>
);
