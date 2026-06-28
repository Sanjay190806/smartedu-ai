import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { titleCase } from "@/lib/formatters";

export const ReadinessScoreChart = ({ scores }: { scores: Record<string, unknown> }) => {
  const data = Object.entries(scores || {}).map(([label, value]) => ({ label: titleCase(label), value: Number(value || 0) }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" opacity={0.18} />
        <XAxis dataKey="label" hide />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Bar dataKey="value" fill="#10b981" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};
