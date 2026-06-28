import { Download } from "lucide-react";

import { Button } from "@/components/ui/button";
import { mentorReportToMarkdown, mentorReportToText } from "@/lib/reportExport";
import type { MentorReport } from "@/lib/types";

function download(filename: string, content: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export const ReportDownload = ({ report }: { report: MentorReport }) => (
  <div className="flex flex-wrap gap-2">
    <Button variant="secondary" onClick={() => download(`${report.session_id}.json`, JSON.stringify(report, null, 2), "application/json")}>
      <Download className="h-4 w-4" /> JSON
    </Button>
    <Button variant="secondary" onClick={() => download(`${report.session_id}.md`, mentorReportToMarkdown(report), "text/markdown")}>
      <Download className="h-4 w-4" /> Markdown
    </Button>
    <Button variant="secondary" onClick={() => download(`${report.session_id}.txt`, mentorReportToText(report), "text/plain")}>
      <Download className="h-4 w-4" /> TXT
    </Button>
  </div>
);
