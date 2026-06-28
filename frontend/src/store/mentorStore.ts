import { create } from "zustand";

import type { MentorReport, MentorSession } from "@/lib/types";

interface MentorState {
  activeSession: MentorSession | null;
  activeReport: MentorReport | null;
  setActiveSession: (session: MentorSession | null) => void;
  setActiveReport: (report: MentorReport | null) => void;
}

export const useMentorStore = create<MentorState>((set) => ({
  activeSession: null,
  activeReport: null,
  setActiveSession: (session) => set({ activeSession: session }),
  setActiveReport: (report) => set({ activeReport: report }),
}));
