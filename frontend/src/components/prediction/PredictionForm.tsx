import { useState } from "react";
import { BrainCircuit, GraduationCap, HeartPulse, IdCard, Layers3 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { departments } from "@/lib/constants";
import { sampleProfiles } from "@/lib/samplePayloads";
import type { PredictionRequest } from "@/lib/types";

const selectClass = "h-10 w-full rounded-xl border border-input bg-background/70 px-3 text-sm outline-none transition focus:border-primary/50 focus:ring-2 focus:ring-ring/50";

const academicFields: Array<[keyof PredictionRequest, string, number, number]> = [
  ["attendance_percentage", "Attendance %", 0, 100],
  ["internal_marks_average", "Internal Marks", 0, 100],
  ["assignment_completion_rate", "Assignment Completion", 0, 100],
  ["quiz_average", "Quiz Average", 0, 100],
  ["previous_semester_gpa", "Previous GPA", 0, 10],
  ["current_gpa", "Current GPA", 0, 10],
  ["backlogs", "Backlogs", 0, 20],
  ["late_submissions", "Late Submissions", 0, 30],
];

const subjectFields: Array<[keyof PredictionRequest, string, number, number]> = [
  ["subject_math_score", "Math", 0, 100],
  ["subject_programming_score", "Programming", 0, 100],
  ["subject_electronics_score", "Electronics", 0, 100],
  ["subject_communication_score", "Communication", 0, 100],
  ["subject_lab_score", "Lab", 0, 100],
];

const engagementFields: Array<[keyof PredictionRequest, string, number, number]> = [
  ["study_hours_per_week", "Study Hours/Week", 0, 80],
  ["participation_score", "Participation", 0, 100],
  ["library_usage_hours", "Library Hours", 0, 40],
  ["lms_login_frequency", "LMS Logins", 0, 50],
  ["parent_meeting_count", "Parent Meetings", 0, 20],
  ["mentor_meeting_count", "Mentor Meetings", 0, 20],
  ["extracurricular_hours", "Extracurricular Hours", 0, 30],
];

const wellbeingFields: Array<[keyof PredictionRequest, string, number, number]> = [
  ["stress_level", "Stress Level", 1, 10],
  ["sleep_hours", "Sleep Hours", 0, 12],
];

const steps = [
  ["Identity", IdCard],
  ["Academic", GraduationCap],
  ["Subjects", Layers3],
  ["Wellbeing", HeartPulse],
] as const;

const FieldGrid = ({ fields, form, update }: {
  fields: Array<[keyof PredictionRequest, string, number, number]>;
  form: PredictionRequest;
  update: <K extends keyof PredictionRequest>(key: K, next: PredictionRequest[K]) => void;
}) => (
  <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
    {fields.map(([key, label, min, max]) => (
      <label key={String(key)} className="space-y-1.5">
        <span className="text-xs font-semibold text-muted-foreground">{label}</span>
        <Input
          type="number"
          min={min}
          max={max}
          step="0.1"
          value={String(form[key])}
          onChange={(event) => update(key, Number(event.target.value) as PredictionRequest[typeof key])}
        />
      </label>
    ))}
  </div>
);

export const PredictionForm = ({ value, onChange, onSubmit, loading }: { value?: PredictionRequest; onChange?: (payload: PredictionRequest) => void; onSubmit: (payload: PredictionRequest) => void; loading?: boolean }) => {
  const [form, setForm] = useState<PredictionRequest>(value || sampleProfiles.medium);
  const update = <K extends keyof PredictionRequest>(key: K, next: PredictionRequest[K]) => {
    const updated = { ...form, [key]: next };
    setForm(updated);
    onChange?.(updated);
  };

  const completionScore = Math.round(((form.attendance_percentage + form.assignment_completion_rate + form.internal_marks_average) / 300) * 100);

  return (
    <form className="space-y-6" onSubmit={(event) => { event.preventDefault(); onSubmit(form); }}>
      <div className="step-rail">
        {steps.map(([label, Icon], index) => (
          <span key={label} className={index === 1 ? "step-chip step-chip-active" : "step-chip"}>
            <Icon className="mr-1.5 inline h-3.5 w-3.5" /> {label}
          </span>
        ))}
        <span className="ml-auto hidden rounded-full bg-muted px-3 py-1.5 text-xs font-semibold text-muted-foreground md:inline-flex">
          Profile completeness {completionScore}%
        </span>
      </div>

      <section className="rounded-3xl border border-border bg-background/60 p-4">
        <div className="mb-4 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-primary/10 text-primary"><IdCard className="h-5 w-5" /></div>
          <div>
            <h3 className="font-semibold">Identity</h3>
            <p className="text-xs text-muted-foreground">Student profile used for persistence and recommendation retrieval.</p>
          </div>
        </div>
        <div className="grid gap-3 md:grid-cols-3">
          <Input value={form.student_id} onChange={(event) => update("student_id", event.target.value)} placeholder="Student ID" />
          <Input value={form.name} onChange={(event) => update("name", event.target.value)} placeholder="Name" />
          <select className={selectClass} value={form.department} onChange={(event) => update("department", event.target.value)}>
            {departments.map((department) => <option key={department}>{department}</option>)}
          </select>
          <Input type="number" value={form.year} onChange={(event) => update("year", Number(event.target.value))} placeholder="Year" />
          <Input type="number" value={form.semester} onChange={(event) => update("semester", Number(event.target.value))} placeholder="Semester" />
          <Input value={form.gender} onChange={(event) => update("gender", event.target.value)} placeholder="Gender" />
        </div>
      </section>

      <section className="rounded-3xl border border-border bg-background/60 p-4">
        <div className="mb-4 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-primary/10 text-primary"><GraduationCap className="h-5 w-5" /></div>
          <div>
            <h3 className="font-semibold">Academic Signals</h3>
            <p className="text-xs text-muted-foreground">Core performance indicators used by the ML risk model.</p>
          </div>
        </div>
        <FieldGrid fields={academicFields} form={form} update={update} />
      </section>

      <section className="rounded-3xl border border-border bg-background/60 p-4">
        <div className="mb-4 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-primary/10 text-primary"><Layers3 className="h-5 w-5" /></div>
          <div>
            <h3 className="font-semibold">Subject Performance</h3>
            <p className="text-xs text-muted-foreground">Subject-level context for explainability and intervention planning.</p>
          </div>
        </div>
        <FieldGrid fields={subjectFields} form={form} update={update} />
      </section>

      <section className="rounded-3xl border border-border bg-background/60 p-4">
        <div className="mb-4 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-2xl bg-primary/10 text-primary"><HeartPulse className="h-5 w-5" /></div>
          <div>
            <h3 className="font-semibold">Engagement and Wellbeing</h3>
            <p className="text-xs text-muted-foreground">Study cadence, participation, stress, sleep, and support-touch signals.</p>
          </div>
        </div>
        <FieldGrid fields={engagementFields} form={form} update={update} />
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          <FieldGrid fields={wellbeingFields} form={form} update={update} />
          <label className="space-y-1.5">
            <span className="text-xs font-semibold text-muted-foreground">Internet Access</span>
            <select className={selectClass} value={form.internet_access} onChange={(event) => update("internet_access", event.target.value)}>
              <option>Yes</option>
              <option>No</option>
            </select>
          </label>
        </div>
      </section>

      <Button type="submit" size="lg" disabled={loading}>
        <BrainCircuit className="h-4 w-4" /> {loading ? "Predicting..." : "Run Risk Prediction"}
      </Button>
    </form>
  );
};
