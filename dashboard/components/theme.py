from __future__ import annotations

import streamlit as st


THEME_STATE_KEY = "smartedu_theme"
THEME_OPTIONS = ["Dark", "Light", "System"]


THEME_TOKENS = {
    "dark": {
        "bg_primary": "#07111f",
        "bg_secondary": "#0b1728",
        "card_bg": "rgba(15, 30, 50, 0.96)",
        "card_bg_alt": "rgba(9, 20, 36, 0.96)",
        "card_border": "rgba(148, 163, 184, 0.24)",
        "text_primary": "#f8fafc",
        "text_secondary": "#b6c4d7",
        "text_muted": "#94a3b8",
        "accent": "#38bdf8",
        "accent_soft": "rgba(56, 189, 248, 0.14)",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "shadow": "0 14px 38px rgba(0,0,0,0.24)",
        "hero": "linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(14, 42, 68, 0.90))",
        "app_bg": "linear-gradient(180deg, #06101f 0%, #08111f 45%, #050b14 100%)",
    },
    "light": {
        "bg_primary": "#f7fafc",
        "bg_secondary": "#eef4fb",
        "card_bg": "rgba(255, 255, 255, 0.97)",
        "card_bg_alt": "rgba(241, 247, 253, 0.98)",
        "card_border": "rgba(71, 85, 105, 0.18)",
        "text_primary": "#102033",
        "text_secondary": "#334155",
        "text_muted": "#64748b",
        "accent": "#0f7ea8",
        "accent_soft": "rgba(14, 116, 144, 0.10)",
        "success": "#15803d",
        "warning": "#b45309",
        "danger": "#b91c1c",
        "shadow": "0 14px 34px rgba(15, 23, 42, 0.10)",
        "hero": "linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(226, 240, 249, 0.96))",
        "app_bg": "linear-gradient(180deg, #f8fbff 0%, #eef6ff 48%, #f7fafc 100%)",
    },
}


def set_active_theme(theme: str) -> str:
    normalized = theme.lower()
    if normalized not in {"dark", "light", "system"}:
        normalized = "dark"
    st.session_state[THEME_STATE_KEY] = normalized
    return normalized


def get_active_theme() -> str:
    theme = str(st.session_state.get(THEME_STATE_KEY, "dark")).lower()
    if theme == "system":
        return "dark"
    if theme not in {"dark", "light"}:
        return "dark"
    return theme


def get_plotly_template(theme: str | None = None) -> str:
    active = (theme or get_active_theme()).lower()
    return "plotly_white" if active == "light" else "plotly_dark"


def get_risk_colors(theme: str | None = None) -> dict[str, str]:
    active = (theme or get_active_theme()).lower()
    if active == "light":
        return {
            "Low Risk": "#15803d",
            "Medium Risk": "#b45309",
            "High Risk": "#b91c1c",
        }
    return {
        "Low Risk": "#22c55e",
        "Medium Risk": "#f59e0b",
        "High Risk": "#ef4444",
    }


def inject_theme_css(theme: str | None = None) -> None:
    active = (theme or get_active_theme()).lower()
    tokens = THEME_TOKENS["light" if active == "light" else "dark"]
    st.markdown(
        f"""
        <style>
        :root {{
            --bg-primary: {tokens["bg_primary"]};
            --bg-secondary: {tokens["bg_secondary"]};
            --card-bg: {tokens["card_bg"]};
            --card-bg-alt: {tokens["card_bg_alt"]};
            --card-border: {tokens["card_border"]};
            --text-primary: {tokens["text_primary"]};
            --text-secondary: {tokens["text_secondary"]};
            --text-muted: {tokens["text_muted"]};
            --accent: {tokens["accent"]};
            --accent-soft: {tokens["accent_soft"]};
            --success: {tokens["success"]};
            --warning: {tokens["warning"]};
            --danger: {tokens["danger"]};
            --shadow-soft: {tokens["shadow"]};
        }}
        .stApp {{
            background: {tokens["app_bg"]};
            color: var(--text-primary);
        }}
        section[data-testid="stSidebar"] {{
            background: var(--bg-secondary);
            border-right: 1px solid var(--card-border);
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            letter-spacing: 0 !important;
            color: var(--text-primary) !important;
        }}
        p, li, label, span, div {{
            color: inherit;
        }}
        .smart-hero {{
            padding: 2rem;
            border: 1px solid var(--card-border);
            border-radius: 18px;
            background: {tokens["hero"]};
            box-shadow: var(--shadow-soft);
            margin-bottom: 1.25rem;
        }}
        .smart-hero h1 {{
            margin: 0;
            font-size: clamp(2.2rem, 5vw, 4.2rem);
            line-height: 1.02;
        }}
        .smart-hero p {{
            color: var(--text-secondary);
            font-size: 1.05rem;
            max-width: 900px;
        }}
        .smart-card, .metric-card, .insight-card, .empty-state, .command-box, .timeline-item, .mentor-note, .report-card {{
            border: 1px solid var(--card-border);
            background: linear-gradient(180deg, var(--card-bg), var(--card-bg-alt));
            border-radius: 16px;
            padding: 1.05rem;
            box-shadow: var(--shadow-soft);
            margin-bottom: 0.9rem;
            color: var(--text-primary);
        }}
        .metric-card {{
            min-height: 132px;
            position: relative;
            overflow: hidden;
        }}
        .metric-card:before {{
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 4px;
            background: var(--accent);
        }}
        .metric-label, .small-label {{
            color: var(--text-muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }}
        .metric-value {{
            color: var(--text-primary);
            font-size: 2rem;
            font-weight: 800;
            margin-top: 0.35rem;
            overflow-wrap: anywhere;
        }}
        .metric-subtitle, .muted-text {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.35rem;
        }}
        .risk-badge, .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            font-weight: 800;
            border: 1px solid var(--card-border);
        }}
        .risk-low, .status-online {{
            background: color-mix(in srgb, var(--success) 16%, transparent);
            color: var(--success);
            border-color: color-mix(in srgb, var(--success) 40%, transparent);
        }}
        .risk-medium {{
            background: color-mix(in srgb, var(--warning) 16%, transparent);
            color: var(--warning);
            border-color: color-mix(in srgb, var(--warning) 40%, transparent);
        }}
        .risk-high, .status-offline {{
            background: color-mix(in srgb, var(--danger) 16%, transparent);
            color: var(--danger);
            border-color: color-mix(in srgb, var(--danger) 40%, transparent);
        }}
        .section-title {{
            margin-top: 1.5rem;
            padding-top: 0.35rem;
            color: var(--text-primary);
            font-weight: 800;
            font-size: 1.25rem;
        }}
        .empty-state {{
            text-align: center;
            padding: 2rem;
            border-style: dashed;
        }}
        .empty-state h3 {{
            margin-bottom: 0.4rem;
        }}
        .command-box code {{
            display: block;
            color: var(--accent);
            white-space: pre-wrap;
            font-size: 0.92rem;
        }}
        .timeline-item {{
            border-left: 4px solid var(--accent);
        }}
        .mentor-note {{
            border-color: color-mix(in srgb, var(--accent) 42%, transparent);
            background: linear-gradient(135deg, var(--accent-soft), var(--card-bg));
        }}
        .smart-chip {{
            display: inline-block;
            padding: 0.35rem 0.65rem;
            margin: 0.2rem 0.25rem 0.2rem 0;
            border: 1px solid var(--card-border);
            border-radius: 999px;
            color: var(--accent);
            background: var(--accent-soft);
            font-size: 0.9rem;
        }}
        .workflow {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            align-items: center;
        }}
        .workflow-step {{
            padding: 0.55rem 0.8rem;
            border: 1px solid var(--card-border);
            border-radius: 999px;
            background: var(--accent-soft);
            color: var(--accent);
            font-weight: 700;
        }}
        .workflow-arrow {{
            color: var(--accent);
            font-weight: 900;
        }}
        div[data-testid="stMetric"] {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 0.9rem;
            border-radius: 14px;
        }}
        .stButton > button, .stDownloadButton > button, .stLinkButton > a {{
            border-radius: 12px !important;
            border: 1px solid color-mix(in srgb, var(--accent) 45%, transparent) !important;
            background: linear-gradient(135deg, var(--accent), #2563eb) !important;
            color: white !important;
            font-weight: 800 !important;
        }}
        input, textarea, div[data-baseweb="select"] > div {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border-color: var(--card-border) !important;
        }}
        div[data-testid="stDataFrame"] {{
            border: 1px solid var(--card-border);
            border-radius: 14px;
            overflow: hidden;
        }}
        .report-list {{
            margin: 0.35rem 0 0 1rem;
            color: var(--text-secondary);
        }}
        .report-kv {{
            display: grid;
            grid-template-columns: minmax(140px, 0.35fr) 1fr;
            gap: 0.5rem;
            padding: 0.45rem 0;
            border-bottom: 1px solid var(--card-border);
        }}
        .report-kv:last-child {{
            border-bottom: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_premium_css() -> None:
    inject_theme_css(get_active_theme())
