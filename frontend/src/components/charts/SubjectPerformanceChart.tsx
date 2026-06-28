import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import type { SubjectPerformance } from "@/lib/types";
import { titleCase } from "@/lib/formatters";

export const SubjectPerformanceChart = ({ subjects }: { subjects: Partial<SubjectPerformance> }) => {
  const data = Object.entries(subjects || {}).map(([subject, score]) => ({ subject: titleCase(subject), score: Number(score || 0) }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" opacity={0.18} />
        <XAxis dataKey="subject" />
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Bar dataKey="score" fill="#38bdf8" radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};
