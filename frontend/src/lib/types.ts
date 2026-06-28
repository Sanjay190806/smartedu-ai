export type RiskLabel = "Low Risk" | "Medium Risk" | "High Risk";

export interface AcademicRecord {
  id?: number;
  student_id?: string;
  attendance_percentage: number;
  internal_marks_average: number;
  assignment_completion_rate: number;
  quiz_average: number;
  previous_semester_gpa: number;
  current_gpa: number;
  study_hours_per_week: number;
  backlogs: number;
  late_submissions: number;
  participation_score: number;
  subject_math_score: number;
  subject_programming_score: number;
  subject_electronics_score: number;
  subject_communication_score: number;
  subject_lab_score: number;
  library_usage_hours: number;
  lms_login_frequency: number;
  parent_meeting_count: number;
  mentor_meeting_count: number;
  extracurricular_hours: number;
  stress_level: number;
  sleep_hours: number;
  internet_access: string;
  created_at?: string;
}

export interface Student {
  id?: number;
  student_id: string;
  name: string;
  department: string;
  year: number;
  semester: number;
  gender: string;
  created_at?: string;
  updated_at?: string;
  latest_academic_record?: AcademicRecord | null;
}

export type PredictionRequest = Student & AcademicRecord;

export interface Recommendation {
  student_id?: string | null;
  risk_category: RiskLabel;
  summary: string;
  top_problems: string[];
  action_plan: string[];
  seven_day_plan: string[];
  thirty_day_plan: string[];
  resources: string[];
  mentor_note: string;
}

export interface PredictionResponse {
  student_id?: string | null;
  risk_category: RiskLabel;
  probability: number;
  confidence: string;
  top_factors: string[];
  explanation: string;
  recommendations: Recommendation;
}

export interface BatchPredictionResponse {
  total_records: number;
  predictions: PredictionResponse[];
  risk_distribution: Record<RiskLabel, number>;
}

export interface AnalyticsSummary {
  total_students: number;
  low_risk_count: number;
  medium_risk_count: number;
  high_risk_count: number;
  average_attendance: number;
  average_gpa: number;
  average_assignment_completion: number;
  top_weak_subjects: string[];
}

export type RiskDistribution = Record<string, number>;

export interface SubjectPerformance {
  math: number;
  programming: number;
  electronics: number;
  communication: number;
  lab: number;
}

export interface ProviderStatus {
  provider: "offline" | "openrouter" | "groq" | string;
  real_ai_configured: boolean;
  fallback_available: boolean;
  active_model: string;
  provider_warning?: string | null;
}

export interface MentorAnswer {
  question_number: number;
  question_text: string;
  answer_text: string;
  detected_signals?: Record<string, unknown>;
  next_question_reason?: string;
  created_at?: string | null;
}

export interface MentorSession {
  session_id: string;
  student_id?: string | null;
  student_name?: string | null;
  academic_context: Record<string, unknown>;
  status: string;
  current_question_number: number;
  max_questions: number;
  clarity_score: number;
  dominant_interest_area?: string | null;
  current_question: string;
  current_question_reason: string;
  answers: MentorAnswer[];
}

export interface MentorAnswerResponse {
  session_id: string;
  status: string;
  current_question_number: number;
  max_questions: number;
  clarity_score: number;
  dominant_interest_area?: string | null;
  previous_answer_analysis: Record<string, unknown>;
  next_question: string;
  why_this_question: string;
  ready_for_report: boolean;
  provider_warning?: string | null;
}

export interface MentorReport {
  session_id: string;
  student_id?: string | null;
  primary_career_path: string;
  secondary_career_paths: Array<Record<string, unknown>>;
  confidence_score: number;
  report: Record<string, unknown>;
  provider_warning?: string | null;
}

export interface UserProfile {
  name: string;
  email: string;
  picture?: string;
  provider: "google" | "demo";
}

export interface ApiErrorShape {
  message: string;
  status?: number;
}
