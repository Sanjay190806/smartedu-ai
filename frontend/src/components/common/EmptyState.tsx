import { Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";

export const EmptyState = ({ title, message }: { title: string; message: string }) => (
  <Card className="border-dashed text-center">
    <Sparkles className="mx-auto h-8 w-8 text-primary" />
    <h3 className="mt-3 text-lg font-semibold">{title}</h3>
    <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">{message}</p>
  </Card>
);
