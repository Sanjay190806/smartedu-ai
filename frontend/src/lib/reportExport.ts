import type { MentorReport } from "./types";

const stringifyList = (items: unknown) => {
  if (!Array.isArray(items)) return "-";
  return items
    .map((item) => {
      if (typeof item === "object" && item !== null) {
        const record = item as Record<string, unknown>;
        return record.project_title || record.career || record.path || record.reason || JSON.stringify(record);
      }
      return String(item);
    })
    .join(", ");
};

export function mentorReportToMarkdown(payload: MentorReport) {
  const report = payload.report;
  const executive = report.executive_summary as Record<string, unknown> | undefined;
  const career = report.career_path_recommendation as Record<string, unknown> | undefined;
  const roadmap = report.personalized_skill_roadmap as Record<string, unknown> | undefined;
  const weekly = report.weekly_plan as Record<string, string[]> | undefined;
  const projects = report.project_recommendations;
  const advice = report.mentor_advice as Record<string, unknown> | undefined;

  return `# SmartEdu AI Mentor Report

## Executive Summary
${executive?.one_paragraph_summary || "Not available"}

## Career Recommendation
- Primary path: ${career?.primary_path || payload.primary_career_path}
- Why it fits: ${career?.why_this_path_fits || "-"}

## Skill Roadmap
- Next 30 days: ${stringifyList(roadmap?.next_30_days)}
- Next 90 days: ${stringifyList(roadmap?.next_90_days)}

## Weekly Plan
${weekly ? Object.entries(weekly).map(([day, tasks]) => `- ${day}: ${tasks.join(", ")}`).join("\n") : "- Not available"}

## Projects
${stringifyList(projects)}

## Mentor Advice
- Advice: ${advice?.short_advice || "-"}
- Hard truth: ${advice?.hard_truth || "-"}
- Next action: ${advice?.next_best_action || "-"}
`;
}

export const mentorReportToText = (payload: MentorReport) =>
  mentorReportToMarkdown(payload).replaceAll("#", "").replaceAll("**", "").trim();
