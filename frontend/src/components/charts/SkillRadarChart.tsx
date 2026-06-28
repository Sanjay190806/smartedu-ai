import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";

export const SkillRadarChart = ({ skills }: { skills: string[] }) => {
  const data = (skills.length ? skills : ["Python", "SQL", "Projects", "Communication", "Consistency"]).map((skill, index) => ({
    skill,
    score: Math.max(45, 90 - index * 8),
  }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <RadarChart data={data}>
        <PolarGrid opacity={0.22} />
        <PolarAngleAxis dataKey="skill" />
        <Radar dataKey="score" fill="#8b5cf6" fillOpacity={0.35} stroke="#8b5cf6" />
        <Tooltip />
      </RadarChart>
    </ResponsiveContainer>
  );
};
