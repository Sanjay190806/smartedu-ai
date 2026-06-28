import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export const GlassCard = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <Card className={cn("glass-card", className)}>{children}</Card>
);
