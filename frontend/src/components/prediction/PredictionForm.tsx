import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { departments } from "@/lib/constants";
import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";

const numericFields: Array<[keyof PredictionRequest, string, number, number]> = [
  ["attendance_percentage", "Attendance %", 0, 100],
  ["internal_marks_average", "Internal Marks", 0, 100],
  ["assignment_completion_rate", "Assignment Completion", 0, 100],
  ["quiz_average", "Quiz Average", 0, 100],
  ["previous_semester_gpa", "Previous GPA", 0, 10],
  ["current_gpa", "Current GPA", 0, 10],
  ["study_hours_per_week", "Study Hours/Week", 0, 80],
  ["backlogs", "Backlogs", 0, 20],
  ["late_submissions", "Late Submissions", 0, 30],
  ["participation_score", "Participation", 0, 100],
  ["subject_math_score", "Math Score", 0, 100],
  ["subject_programming_score", "Programming Score", 0, 100],
  ["subject_electronics_score", "Electronics Score", 0, 100],
  ["subject_communication_score", "Communication Score", 0, 100],
  ["subject_lab_score", "Lab Score", 0, 100],
  ["library_usage_hours", "Library Hours", 0, 40],
  ["lms_login_frequency", "LMS Logins", 0, 50],
  ["parent_meeting_count", "Parent Meetings", 0, 20],
  ["mentor_meeting_count", "Mentor Meetings", 0, 20],
  ["extracurricular_hours", "Extracurricular Hours", 0, 30],
  ["stress_level", "Stress Level", 1, 10],
  ["sleep_hours", "Sleep Hours", 0, 12],
];

export const PredictionForm = ({ value, onChange, onSubmit, loading }: { value?: PredictionRequest; onChange?: (payload: PredictionRequest) => void; onSubmit: (payload: PredictionRequest) => void; loading?: boolean }) => {
  const [form, setForm] = useState<PredictionRequest>(value || sampleProfiles.medium);
  const update = <K extends keyof PredictionRequest>(key: K, next: PredictionRequest[K]) => {
    const updated = { ...form, [key]: next };
    setForm(updated);
    onChange?.(updated);
  };

  return (
    <form className="space-y-6" onSubmit={(event) => { event.preventDefault(); onSubmit(form); }}>
      <section className="grid gap-3 md:grid-cols-3">
        <Input value={form.student_id} onChange={(event) => update("student_id", event.target.value)} placeholder="Student ID" />
        <Input value={form.name} onChange={(event) => update("name", event.target.value)} placeholder="Name" />
        <select className="h-10 rounded-xl border border-input bg-background px-3 text-sm" value={form.department} onChange={(event) => update("department", event.target.value)}>
          {departments.map((department) => <option key={department}>{department}</option>)}
        </select>
        <Input type="number" value={form.year} onChange={(event) => update("year", Number(event.target.value))} placeholder="Year" />
        <Input type="number" value={form.semester} onChange={(event) => update("semester", Number(event.target.value))} placeholder="Semester" />
        <Input value={form.gender} onChange={(event) => update("gender", event.target.value)} placeholder="Gender" />
      </section>
      <section className="grid gap-3 md:grid-cols-3 xl:grid-cols-4">
        {numericFields.map(([key, label, min, max]) => (
          <label key={String(key)} className="space-y-1">
            <span className="text-xs font-medium text-muted-foreground">{label}</span>
            <Input type="number" min={min} max={max} step="0.1" value={String(form[key])} onChange={(event) => update(key, Number(event.target.value) as PredictionRequest[typeof key])} />
          </label>
        ))}
        <label className="space-y-1">
          <span className="text-xs font-medium text-muted-foreground">Internet Access</span>
          <select className="h-10 w-full rounded-xl border border-input bg-background px-3 text-sm" value={form.internet_access} onChange={(event) => update("internet_access", event.target.value)}>
            <option>Yes</option>
            <option>No</option>
          </select>
        </label>
      </section>
      <Button type="submit" size="lg" disabled={loading}>{loading ? "Predicting..." : "Run Risk Prediction"}</Button>
    </form>
  );
};
