import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, BrainCircuit, FileText, GraduationCap, Search, ShieldCheck, Users } from "lucide-react";

import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { LoadingState } from "@/components/common/LoadingState";
import { MetricCard } from "@/components/cards/MetricCard";
import { SubjectPerformanceChart } from "@/components/charts/SubjectPerformanceChart";
import { PageShell } from "@/components/layout/PageShell";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { gpa, percent } from "@/lib/formatters";
import type { Student } from "@/lib/types";

const signalFor = (student: Student) => {
  const record = student.latest_academic_record;
  if (!record) return { label: "No record", className: "border-muted bg-muted/60 text-muted-foreground" };
  if (record.current_gpa < 6 || record.attendance_percentage < 75) return { label: "Needs review", className: "border-danger/25 bg-danger/10 text-danger" };
  if (record.current_gpa < 7 || record.attendance_percentage < 82) return { label: "Monitor", className: "border-warning/25 bg-warning/10 text-warning" };
  return { label: "Stable", className: "border-success/25 bg-success/10 text-success" };
};

export const StudentsPage = () => {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Student | null>(null);
  const students = useQuery({ queryKey: ["students"], queryFn: api.getStudents });
  const filtered = useMemo(
    () => (students.data || []).filter((student) => `${student.name} ${student.student_id} ${student.department}`.toLowerCase().includes(query.toLowerCase())),
    [students.data, query],
  );
  const records = students.data || [];
  const selectedRecord = selected?.latest_academic_record;
  const avgAttendance = records.length
    ? records.reduce((sum, student) => sum + (student.latest_academic_record?.attendance_percentage || 0), 0) / records.length
    : 0;
  const withAcademicRecords = records.filter((student) => student.latest_academic_record).length;

  return (
    <PageShell title="Students" description="Search, inspect, and route locally persisted student records into prediction or mentor workflows.">
      {students.isLoading ? <LoadingState /> : students.isError ? <ErrorState message={(students.error as Error).message} /> : (
        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-3">
            <MetricCard label="Student Records" value={records.length} helper="Saved profiles" icon={Users} progress={100} />
            <MetricCard label="Academic Records" value={withAcademicRecords} helper="Profiles with metrics" icon={GraduationCap} progress={records.length ? (withAcademicRecords / records.length) * 100 : 0} />
            <MetricCard label="Avg Attendance" value={percent(avgAttendance)} helper="Across visible records" icon={BookOpen} progress={avgAttendance} />
          </div>

          <div className="grid gap-5 lg:grid-cols-[1.15fr_.85fr]">
            <Card>
              <CardHeader>
                <CardTitle>Student Directory</CardTitle>
                <CardDescription>Search by name, ID, or department. Select a row to inspect academic detail.</CardDescription>
              </CardHeader>
              <div className="mb-4 flex items-center gap-2 rounded-2xl border border-border bg-background/60 px-3">
                <Search className="h-4 w-4 text-muted-foreground" />
                <Input className="border-0 bg-transparent focus:ring-0" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by name, ID, or department" />
              </div>
              {filtered.length ? (
                <div className="max-h-[34rem] overflow-auto pr-1">
                  <table className="data-table">
                    <thead><tr><th>Student</th><th>Department</th><th>GPA</th><th>Attendance</th><th>Status</th><th /></tr></thead>
                    <tbody>
                      {filtered.map((student) => {
                        const signal = signalFor(student);
                        return (
                          <tr key={student.student_id}>
                            <td>
                              <p className="font-semibold">{student.name}</p>
                              <p className="text-xs text-muted-foreground">{student.student_id}</p>
                            </td>
                            <td>{student.department}</td>
                            <td>{gpa(student.latest_academic_record?.current_gpa)}</td>
                            <td>{percent(student.latest_academic_record?.attendance_percentage)}</td>
                            <td><span className={`inline-flex rounded-full border px-2.5 py-1 text-xs font-bold ${signal.className}`}>{signal.label}</span></td>
                            <td><Button size="sm" variant="secondary" onClick={() => setSelected(student)}>View</Button></td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ) : <EmptyState title="No students found" message="Run a prediction or adjust the search filters." />}
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Profile Intelligence</CardTitle>
                <CardDescription>Latest subject performance and workflow actions for the selected student.</CardDescription>
              </CardHeader>
              {selected ? (
                <div className="space-y-5">
                  <div className="rounded-3xl border border-border bg-background/60 p-5">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-2xl font-semibold">{selected.name}</h3>
                        <p className="mt-1 text-sm text-muted-foreground">{selected.department} - Year {selected.year} - Semester {selected.semester}</p>
                      </div>
                      <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${signalFor(selected).className}`}>{signalFor(selected).label}</span>
                    </div>
                    <div className="mt-5 grid gap-3 sm:grid-cols-3">
                      <div className="rounded-2xl border border-border bg-card/70 p-3">
                        <p className="text-xs text-muted-foreground">GPA</p>
                        <p className="text-xl font-bold">{gpa(selectedRecord?.current_gpa)}</p>
                      </div>
                      <div className="rounded-2xl border border-border bg-card/70 p-3">
                        <p className="text-xs text-muted-foreground">Attendance</p>
                        <p className="text-xl font-bold">{percent(selectedRecord?.attendance_percentage)}</p>
                      </div>
                      <div className="rounded-2xl border border-border bg-card/70 p-3">
                        <p className="text-xs text-muted-foreground">Backlogs</p>
                        <p className="text-xl font-bold">{selectedRecord?.backlogs ?? "-"}</p>
                      </div>
                    </div>
                  </div>
                  {selectedRecord ? <SubjectPerformanceChart subjects={{
                    math: selectedRecord.subject_math_score,
                    programming: selectedRecord.subject_programming_score,
                    electronics: selectedRecord.subject_electronics_score,
                    communication: selectedRecord.subject_communication_score,
                    lab: selectedRecord.subject_lab_score,
                  }} /> : <EmptyState title="No academic record" message="This student has no attached academic metrics." />}
                  <div className="grid gap-3 sm:grid-cols-2">
                    <Button asChild><Link to="/app/predict"><ShieldCheck className="h-4 w-4" /> Run prediction</Link></Button>
                    <Button asChild variant="secondary"><Link to="/app/report/latest"><FileText className="h-4 w-4" /> Open mentor report</Link></Button>
                    <Button asChild variant="secondary" className="sm:col-span-2"><Link to="/app/mentor"><BrainCircuit className="h-4 w-4" /> Start mentor interview</Link></Button>
                  </div>
                </div>
              ) : <EmptyState title="Select a student" message="Open a profile to see latest academic metrics, subject trends, and action shortcuts." />}
            </Card>
          </div>
        </div>
      )}
    </PageShell>
  );
};
