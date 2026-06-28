import { Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";

export const EmptyState = ({ title, message }: { title: string; message: string }) => (
  <Card className="border-dashed bg-card/70 text-center">
    <div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl border border-primary/20 bg-primary/10 text-primary">
      <Sparkles className="h-7 w-7" />
    </div>
    <h3 className="mt-3 text-lg font-semibold">{title}</h3>
    <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">{message}</p>
  </Card>
);
