from __future__ import annotations

import streamlit as st


def inject_premium_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #07111f;
            --panel: #0d1b2e;
            --panel-2: #10233a;
            --border: rgba(148, 163, 184, 0.22);
            --text: #e5edf7;
            --muted: #94a3b8;
            --cyan: #22d3ee;
            --blue: #60a5fa;
            --violet: #a78bfa;
            --green: #22c55e;
            --amber: #f59e0b;
            --red: #ef4444;
        }
        .stApp {
            background:
              radial-gradient(circle at top left, rgba(34, 211, 238, 0.16), transparent 34rem),
              radial-gradient(circle at top right, rgba(167, 139, 250, 0.12), transparent 30rem),
              linear-gradient(180deg, #06101f 0%, #08111f 45%, #050b14 100%);
            color: var(--text);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #081321 0%, #0a1729 100%);
            border-right: 1px solid var(--border);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }
        h1, h2, h3 { letter-spacing: 0 !important; color: #f8fafc; }
        .smart-hero {
            padding: 2rem;
            border: 1px solid rgba(34, 211, 238, 0.22);
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(14, 42, 68, 0.9));
            box-shadow: 0 24px 70px rgba(0,0,0,0.32);
            margin-bottom: 1.25rem;
        }
        .smart-hero h1 {
            margin: 0;
            font-size: clamp(2.2rem, 5vw, 4.2rem);
            line-height: 1.02;
        }
        .smart-hero p { color: #cbd5e1; font-size: 1.05rem; max-width: 900px; }
        .smart-card, .metric-card, .insight-card, .empty-state, .command-box, .timeline-item, .mentor-note {
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(15, 30, 50, 0.95), rgba(9, 20, 36, 0.95));
            border-radius: 16px;
            padding: 1.05rem;
            box-shadow: 0 14px 38px rgba(0,0,0,0.22);
            margin-bottom: 0.9rem;
        }
        .metric-card {
            min-height: 132px;
            position: relative;
            overflow: hidden;
        }
        .metric-card:before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 4px;
            background: var(--blue);
        }
        .metric-label, .small-label {
            color: var(--muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }
        .metric-value {
            color: #f8fafc;
            font-size: 2rem;
            font-weight: 800;
            margin-top: 0.35rem;
        }
        .metric-subtitle { color: #aab8cb; font-size: 0.9rem; margin-top: 0.35rem; }
        .risk-badge, .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            font-weight: 800;
            color: white;
            border: 1px solid rgba(255,255,255,0.16);
        }
        .risk-low, .status-online { background: rgba(34, 197, 94, 0.18); color: #bbf7d0; border-color: rgba(34,197,94,0.38); }
        .risk-medium { background: rgba(245, 158, 11, 0.18); color: #fde68a; border-color: rgba(245,158,11,0.38); }
        .risk-high, .status-offline { background: rgba(239, 68, 68, 0.18); color: #fecaca; border-color: rgba(239,68,68,0.38); }
        .section-title {
            margin-top: 1.5rem;
            padding-top: 0.35rem;
            color: #f8fafc;
            font-weight: 800;
            font-size: 1.25rem;
        }
        .empty-state {
            text-align: center;
            padding: 2rem;
            border-style: dashed;
        }
        .empty-state h3 { margin-bottom: 0.4rem; }
        .command-box code {
            display: block;
            color: #bae6fd;
            white-space: pre-wrap;
            font-size: 0.92rem;
        }
        .timeline-item { border-left: 4px solid var(--cyan); }
        .mentor-note {
            border-color: rgba(34, 211, 238, 0.38);
            background: linear-gradient(135deg, rgba(8, 47, 73, 0.85), rgba(15, 23, 42, 0.95));
        }
        .smart-chip {
            display: inline-block;
            padding: 0.35rem 0.65rem;
            margin: 0.2rem 0.25rem 0.2rem 0;
            border: 1px solid var(--border);
            border-radius: 999px;
            color: #dbeafe;
            background: rgba(96, 165, 250, 0.12);
            font-size: 0.9rem;
        }
        .workflow {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            align-items: center;
        }
        .workflow-step {
            padding: 0.55rem 0.8rem;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(15, 30, 50, 0.8);
            color: #e0f2fe;
            font-weight: 700;
        }
        .workflow-arrow { color: var(--cyan); font-weight: 900; }
        div[data-testid="stMetric"] {
            background: rgba(15, 30, 50, 0.72);
            border: 1px solid var(--border);
            padding: 0.9rem;
            border-radius: 14px;
        }
        .stButton > button, .stDownloadButton > button, .stLinkButton > a {
            border-radius: 12px !important;
            border: 1px solid rgba(96,165,250,0.45) !important;
            background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(8,145,178,0.9)) !important;
            color: white !important;
            font-weight: 800 !important;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
