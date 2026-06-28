import type { RiskLabel } from "@/lib/types";
import { cn } from "@/lib/utils";

export const RiskBadge = ({ risk }: { risk?: RiskLabel | string }) => {
  const className =
    risk === "Low Risk"
      ? "border-success/30 bg-success/10 text-success"
      : risk === "Medium Risk"
        ? "border-warning/30 bg-warning/10 text-warning"
        : "border-danger/30 bg-danger/10 text-danger";
  return <span className={cn("inline-flex rounded-full border px-3 py-1 text-xs font-bold", className)}>{risk || "Unknown"}</span>;
};
