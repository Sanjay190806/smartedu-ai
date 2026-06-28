import axios, { AxiosError } from "axios";

import { API_BASE_URL } from "./constants";
import type {
  AnalyticsSummary,
  BatchPredictionResponse,
  MentorAnswerResponse,
  MentorReport,
  MentorSession,
  PredictionRequest,
  PredictionResponse,
  ProviderStatus,
  Recommendation,
  RiskDistribution,
  Student,
  SubjectPerformance,
} from "./types";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 12000,
  headers: {
    "Content-Type": "application/json",
  },
});

function friendlyError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: unknown }>;
    if (axiosError.code === "ECONNABORTED") return new Error("Request timed out. Check that the backend is responding.");
    if (!axiosError.response) return new Error("Backend is offline. Start it with: uvicorn backend.main:app --reload");
    const detail = axiosError.response.data?.detail;
    if (Array.isArray(detail)) {
      return new Error(detail.map((item) => item?.msg || JSON.stringify(item)).join("; "));
    }
    if (typeof detail === "string") return new Error(detail);
    return new Error(`Request failed with HTTP ${axiosError.response.status}.`);
  }
  return new Error("Unexpected API error. Please retry.");
}

async function request<T>(promise: Promise<{ data: T }>): Promise<T> {
  try {
    const response = await promise;
    return response.data;
  } catch (error) {
    throw friendlyError(error);
  }
}

export const api = {
  healthCheck: () => request<Record<string, unknown>>(client.get("/health")),
  getStudents: () => request<Student[]>(client.get("/students")),
  getStudent: (studentId: string) => request<Student>(client.get(`/students/${studentId}`)),
  predictStudent: (payload: PredictionRequest) => request<PredictionResponse>(client.post("/predict", payload)),
  batchPredict: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<BatchPredictionResponse>(
      client.post("/predict/batch", formData, { headers: { "Content-Type": "multipart/form-data" } }),
    );
  },
  getAnalyticsSummary: () => request<AnalyticsSummary>(client.get("/analytics/summary")),
  getRiskDistribution: () => request<RiskDistribution>(client.get("/analytics/risk-distribution")),
  getSubjectPerformance: () => request<SubjectPerformance>(client.get("/analytics/subject-performance")),
  getRecommendation: (studentId: string) => request<Recommendation>(client.get(`/recommendations/${studentId}`)),
  startMentorSession: (payload: Record<string, unknown>) => request<MentorSession>(client.post("/mentor/start", payload)),
  submitMentorAnswer: (sessionId: string, answer: string) =>
    request<MentorAnswerResponse>(client.post(`/mentor/${sessionId}/answer`, { answer })),
  getMentorSession: (sessionId: string) => request<MentorSession>(client.get(`/mentor/${sessionId}`)),
  generateMentorReport: (sessionId: string) => request<MentorReport>(client.post(`/mentor/${sessionId}/report`)),
  getMentorReport: (sessionId: string) => request<MentorReport>(client.get(`/mentor/${sessionId}/report`)),
  getMentorProviderStatus: () => request<ProviderStatus>(client.get("/mentor/provider-status")),
  listMentorSessions: () => request<MentorSession[]>(client.get("/mentor/sessions")),
};
