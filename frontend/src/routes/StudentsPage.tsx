import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search } from "lucide-react";

import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { SubjectPerformanceChart } from "@/components/charts/SubjectPerformanceChart";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";
import type { Student } from "@/lib/types";

export const StudentsPage = () => {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Student | null>(null);
  const students = useQuery({ queryKey: ["students"], queryFn: api.getStudents });
  const filtered = useMemo(() => (students.data || []).filter((student) => `${student.name} ${student.student_id} ${student.department}`.toLowerCase().includes(query.toLowerCase())), [students.data, query]);

  return (
    <PageShell title="Students" description="Search and inspect locally persisted student records.">
      {students.isLoading ? <LoadingState /> : students.isError ? <ErrorState message={(students.error as Error).message} /> : (
        <div className="grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
          <Card>
            <div className="mb-4 flex items-center gap-2 rounded-xl border border-border bg-background px-3">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input className="border-0 bg-transparent" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by name, ID, or department" />
            </div>
            {filtered.length ? (
              <div className="overflow-auto">
                <table className="w-full text-left text-sm">
                  <thead className="text-muted-foreground"><tr><th className="p-3">Student</th><th>Department</th><th>GPA</th><th>Attendance</th><th /></tr></thead>
                  <tbody>
                    {filtered.map((student) => (
                      <tr key={student.student_id} className="border-t border-border">
                        <td className="p-3 font-medium">{student.name}<br /><span className="text-xs text-muted-foreground">{student.student_id}</span></td>
                        <td>{student.department}</td>
                        <td>{gpa(student.latest_academic_record?.current_gpa)}</td>
                        <td>{percent(student.latest_academic_record?.attendance_percentage)}</td>
                        <td><Button size="sm" variant="secondary" onClick={() => setSelected(student)}>View</Button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : <EmptyState title="No students found" message="Run a prediction or adjust the search filters." />}
          </Card>
          <Card>
            <CardHeader><CardTitle>Student Profile</CardTitle></CardHeader>
            {selected ? (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold">{selected.name}</h3>
                  <p className="text-muted-foreground">{selected.department} · Year {selected.year} · Semester {selected.semester}</p>
                </div>
                {selected.latest_academic_record ? <SubjectPerformanceChart subjects={{
                  math: selected.latest_academic_record.subject_math_score,
                  programming: selected.latest_academic_record.subject_programming_score,
                  electronics: selected.latest_academic_record.subject_electronics_score,
                  communication: selected.latest_academic_record.subject_communication_score,
                  lab: selected.latest_academic_record.subject_lab_score,
                }} /> : <EmptyState title="No academic record" message="This student has no attached academic metrics." />}
              </div>
            ) : <EmptyState title="Select a student" message="Open a profile to see latest academic metrics and subjects." />}
          </Card>
        </div>
      )}
    </PageShell>
  );
};
