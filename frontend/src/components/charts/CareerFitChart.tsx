import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export const CareerFitChart = ({ matrix }: { matrix: Array<Record<string, unknown>> }) => {
  const data = matrix.map((item) => ({ career: String(item.career || item.path || "Path"), score: Number(item.match_score || 0) }));
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="vertical" margin={{ left: 24 }}>
        <CartesianGrid strokeDasharray="3 3" opacity={0.18} />
        <XAxis type="number" domain={[0, 100]} />
        <YAxis type="category" dataKey="career" width={120} />
        <Tooltip />
        <Bar dataKey="score" fill="#22d3ee" radius={[0, 8, 8, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};
