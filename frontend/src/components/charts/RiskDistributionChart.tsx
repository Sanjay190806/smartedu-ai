import { Bar, BarChart, CartesianGrid, Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { riskColors } from "@/lib/constants";

export const RiskDistributionChart = ({ distribution, type = "bar" }: { distribution: Record<string, number>; type?: "bar" | "pie" }) => {
  const data = Object.entries(distribution || {}).map(([risk, count]) => ({ risk, count }));
  if (type === "pie") {
    return (
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie data={data} dataKey="count" nameKey="risk" innerRadius={58} outerRadius={90} paddingAngle={4}>
            {data.map((entry) => <Cell key={entry.risk} fill={riskColors[entry.risk] || "#60a5fa"} />)}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    );
  }
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" opacity={0.18} />
        <XAxis dataKey="risk" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Bar dataKey="count" radius={[8, 8, 0, 0]}>
          {data.map((entry) => <Cell key={entry.risk} fill={riskColors[entry.risk] || "#60a5fa"} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
