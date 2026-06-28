export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";

export const riskOrder = ["Low Risk", "Medium Risk", "High Risk"] as const;

export const riskColors: Record<string, string> = {
  "Low Risk": "#22c55e",
  "Medium Risk": "#f59e0b",
  "High Risk": "#ef4444",
};

export const departments = ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Other"];
