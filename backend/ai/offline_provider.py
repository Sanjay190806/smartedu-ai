from __future__ import annotations

from collections import Counter
import re
from typing import Any

from backend.ai.base import BaseAIProvider
from backend.services.career_path_service import CAREER_PATHS, score_paths
from backend.services.learning_plan_service import generate_learning_plan


KEYWORDS = {
    "data": ["python", "pandas", "data", "math", "maths", "statistics", "ml", "machine learning", "analytics", "sql", "dashboard", "visualization"],
    "software": ["coding", "dsa", "java", "backend", "api", "app", "apps", "systems", "debugging", "full stack"],
    "hardware": ["circuits", "sensors", "arduino", "electronics", "iot", "hardware", "robotics", "embedded"],
    "product": ["communication", "presentation", "user", "business", "planning", "leadership", "product", "metrics"],
    "security": ["security", "hacking", "network", "networks", "linux", "cyber"],
    "design": ["design", "ui", "ux", "frontend", "website", "figma", "creative", "react"],
    "confused": ["confused", "unsure", "don't know", "dont know", "not sure", "no idea"],
}

DOMAIN_TO_PATHS = {
    "data": ["Data Scientist", "Data Analyst", "Machine Learning Engineer"],
    "software": ["Software Engineer", "Backend Developer"],
    "hardware": ["Embedded Systems Engineer", "IoT / Edge AI Engineer"],
    "product": ["Product Analyst", "Business Analyst", "Technical Product Manager"],
    "security": ["Cybersecurity Analyst"],
    "design": ["Frontend Developer", "UI/UX + Product Design"],
}

DOMAIN_LABELS = {
    "data": "data and analytics",
    "software": "software engineering",
    "hardware": "hardware or embedded systems",
    "product": "product and business analysis",
    "security": "cybersecurity",
    "design": "frontend or product design",
}


def analyze_answers(answers: list[dict[str, Any]]) -> dict[str, Any]:
    answer_texts = [answer.get("answer_text", answer.get("answer", "")) for answer in answers]
    text = " ".join(answer_texts).lower()
    signal_counts: Counter[str] = Counter()
    domain_scores: Counter[str] = Counter()
    domain_answer_hits: dict[str, set[int]] = {domain: set() for domain in KEYWORDS if domain != "confused"}

    for index, answer_text in enumerate(answer_texts):
        lowered = answer_text.lower()
        for domain, words in KEYWORDS.items():
            if domain == "confused":
                continue
            for word in words:
                hits = len(re.findall(rf"\b{re.escape(word)}\b", lowered))
                if hits:
                    signal_counts[word] += hits
                    domain_scores[domain] += hits
                    domain_answer_hits[domain].add(index)

    disliked_areas = _detect_disliked_areas(text)
    for disliked in disliked_areas:
        domain_scores[disliked] -= 2

    repeated_domains = [
        domain for domain, indexes in domain_answer_hits.items()
        if len(indexes) >= 2 and domain_scores[domain] > 0
    ]
    ordered_domains = [
        domain for domain, _ in sorted(domain_scores.items(), key=lambda item: item[1], reverse=True)
        if domain != "confused" and domain_scores[domain] > 0
    ]
    career_hints: list[str] = []
    for domain in ordered_domains:
        for path in DOMAIN_TO_PATHS.get(domain, []):
            if path not in career_hints:
                career_hints.append(path)

    confusion = "high" if any(word in text for word in KEYWORDS["confused"]) else "low" if career_hints else "medium"
    contradictions = _detect_contradictions(domain_scores, disliked_areas)
    clarity = _calculate_clarity(answer_texts, domain_scores, repeated_domains, contradictions, confusion)
    known_skills = _detect_skills(text)
    paths = score_paths(
        {
            "interests": list(signal_counts.keys()),
            "career_hints": career_hints,
            "known_skills": known_skills,
            "signal_counts": dict(signal_counts),
            "disliked_areas": disliked_areas,
            "repeated_domains": repeated_domains,
        }
    )

    return {
        "interests": [item for item, _ in signal_counts.most_common(12)],
        "strengths": _detect_strengths(text),
        "weaknesses": _detect_weaknesses(text),
        "career_hints": career_hints[:8],
        "known_skills": known_skills,
        "learning_style": _detect_learning_style(text),
        "motivation_level": _detect_motivation(text),
        "confusion_level": confusion,
        "clarity_score": clarity,
        "signal_counts": dict(signal_counts),
        "domain_scores": dict(domain_scores),
        "repeated_domains": repeated_domains,
        "disliked_areas": disliked_areas,
        "contradictions": contradictions,
        "daily_time_hours": _detect_daily_time(text),
        "career_goal": _detect_career_goal(text),
        "project_preferences": _detect_project_preferences(text),
        "skill_level": _detect_skill_level(text, known_skills),
        "recommended_primary_path": paths[0]["path"] if paths else "Career Exploration",
    }


def _calculate_clarity(
    answer_texts: list[str],
    domain_scores: Counter[str],
    repeated_domains: list[str],
    contradictions: list[str],
    confusion: str,
) -> float:
    top_score = max(domain_scores.values()) if domain_scores else 0
    vague_penalty = 0.1 if answer_texts and sum(len(answer.split()) for answer in answer_texts) / len(answer_texts) < 6 else 0
    clarity = 0.18 + min(len(answer_texts) * 0.06, 0.42) + min(top_score * 0.035, 0.22)
    if repeated_domains:
        clarity += 0.12
    if contradictions:
        clarity -= 0.12
    if confusion == "high":
        clarity = min(clarity, 0.5)
    clarity -= vague_penalty
    return round(max(0.2, min(0.93, clarity)), 2)


def _detect_disliked_areas(text: str) -> list[str]:
    disliked = []
    patterns = {
        "hardware": ["don't like hardware", "dont like hardware", "not hardware", "avoid hardware", "dislike hardware", "not interested in hardware", "don't like electronics"],
        "software": ["don't like coding", "dont like coding", "not coding", "avoid coding"],
        "data": ["don't like data", "dont like data", "avoid statistics", "not statistics"],
        "product": ["don't like presentation", "avoid communication", "not business"],
    }
    for domain, phrases in patterns.items():
        if any(phrase in text for phrase in phrases):
            disliked.append(domain)
    return disliked


def _detect_contradictions(domain_scores: Counter[str], disliked_areas: list[str]) -> list[str]:
    return [
        f"{DOMAIN_LABELS.get(domain, domain)} was mentioned but also disliked"
        for domain in disliked_areas
        if domain_scores.get(domain, 0) > 0
    ]


def _detect_strengths(text: str) -> list[str]:
    strengths = []
    for word, label in [
        ("math", "logic and quantitative thinking"),
        ("statistics", "statistical reasoning"),
        ("problem", "problem solving"),
        ("communication", "communication"),
        ("project", "project building"),
        ("debug", "persistence with debugging"),
        ("explain", "explaining ideas clearly"),
    ]:
        if word in text:
            strengths.append(label)
    return sorted(set(strengths)) or ["curiosity and willingness to reflect"]


def _detect_weaknesses(text: str) -> list[str]:
    weaknesses = []
    for word, label in [
        ("weak", "weak basics"),
        ("dsa", "DSA practice"),
        ("communication", "communication polish"),
        ("hardware", "hardware comfort"),
        ("time", "time consistency"),
        ("sql", "SQL practice"),
        ("statistics", "statistics basics"),
    ]:
        if ("not " + word) in text or ("weak " + word) in text or ("difficult" in text and word in text) or ("need" in text and word in text):
            weaknesses.append(label)
    return sorted(set(weaknesses)) or ["needs a clearer execution routine"]


def _detect_skills(text: str) -> list[str]:
    skills = []
    for skill in ["python", "java", "sql", "pandas", "excel", "power bi", "arduino", "react", "figma", "linux", "fastapi", "django"]:
        if skill in text:
            skills.append(skill.title() if skill != "sql" else "SQL")
    return sorted(set(skills))


def _detect_learning_style(text: str) -> str:
    if "project" in text or "github" in text or "portfolio" in text:
        return "project-based"
    if "video" in text or "youtube" in text:
        return "video-led"
    if "book" in text or "notes" in text:
        return "notes-and-revision"
    return "practice-first"


def _detect_motivation(text: str) -> str:
    if any(word in text for word in ["daily", "consistent", "internship", "placement", "high-paying", "stable"]):
        return "high"
    if any(word in text for word in ["confused", "not sure", "no idea"]):
        return "uncertain"
    return "medium"


def _detect_daily_time(text: str) -> float | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:hours|hour|hrs|hr)", text)
    if not match:
        return None
    return float(match.group(1))


def _detect_career_goal(text: str) -> list[str]:
    goals = []
    for word, label in [
        ("internship", "internship readiness"),
        ("placement", "placement readiness"),
        ("stable", "stable career"),
        ("high-paying", "high-paying career"),
        ("portfolio", "portfolio strength"),
        ("github", "GitHub proof of work"),
    ]:
        if word in text:
            goals.append(label)
    return goals or ["career clarity"]


def _detect_project_preferences(text: str) -> list[str]:
    preferences = []
    for word, label in [
        ("dashboard", "dashboard project"),
        ("notebook", "analysis notebook"),
        ("api", "backend API project"),
        ("app", "application project"),
        ("sensor", "sensor prototype"),
        ("portfolio", "portfolio project"),
    ]:
        if word in text:
            preferences.append(label)
    return preferences


def _detect_skill_level(text: str, known_skills: list[str]) -> str:
    if any(word in text for word in ["beginner", "basic", "starting"]):
        return "beginner"
    if any(word in text for word in ["advanced", "strong", "expert"]):
        return "advanced"
    if len(known_skills) >= 3:
        return "early intermediate"
    return "foundation-building"


class OfflineMentorProvider(BaseAIProvider):
    name = "offline"
    model_name = "offline-rule-based"

    def generate_next_question(self, context: dict[str, Any]) -> dict[str, Any]:
        answers = context.get("answers", [])
        signals = analyze_answers(answers)
        asked = {answer.get("question_text", "").lower() for answer in answers}
        question, reason = choose_question(signals, asked, len(answers) + 1, context.get("academic_context", {}))
        ready = len(answers) >= 8 or signals["clarity_score"] >= 0.75 or len(answers) >= context.get("max_questions", 15)
        return {
            "previous_answer_analysis": {
                "detected_interests": signals["interests"],
                "detected_strengths": signals["strengths"],
                "detected_weaknesses": signals["weaknesses"],
                "possible_paths": [signals["recommended_primary_path"]] + [
                    path for path in signals["career_hints"] if path != signals["recommended_primary_path"]
                ],
                "learning_style": signals["learning_style"],
                "motivation_level": signals["motivation_level"],
                "confusion_level": signals["confusion_level"],
                "clarity_score": signals["clarity_score"],
            },
            "next_question": question,
            "why_this_question": reason,
            "ready_for_report": ready,
            "detected_signals": signals,
        }

    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        answers = context.get("answers", [])
        academic = context.get("academic_context", {})
        signals = analyze_answers(answers)
        paths = score_paths(signals)
        primary = paths[0]
        secondary = paths[1:4]
        learning = generate_learning_plan(primary["path"], signals, academic)
        confidence = min(0.94, max(signals["clarity_score"], 0.38 + len(answers) * 0.045))
        return build_report(context, signals, primary, secondary, learning, round(confidence, 2), paths)


def choose_question(signals: dict[str, Any], asked: set[str], number: int, academic: dict[str, Any] | None = None) -> tuple[str, str]:
    academic = academic or {}
    domain_scores = signals.get("domain_scores", {})
    disliked = set(signals.get("disliked_areas", []))
    top_domain = max(domain_scores, key=domain_scores.get) if domain_scores else ""
    candidates: list[tuple[str, str]] = []

    if signals.get("confusion_level") == "high" or not top_domain:
        candidates.append(("Which task feels least painful for you: debugging code, analyzing data, designing a feature, explaining ideas, or building hardware circuits?", "This reduces confusion by comparing real work activities instead of abstract career names."))
    if top_domain == "data" or domain_scores.get("data", 0) >= 2:
        candidates.extend([
            ("When you work with data, do you enjoy cleaning datasets, finding insights, building ML models, or creating dashboards more?", "Your repeated Python, maths, data, or analytics signals need a sharper split between Data Analyst, Data Scientist, and ML Engineer."),
            ("How comfortable are you with SQL, statistics, and explaining charts to others?", "Data careers require both technical analysis and communication of insights."),
        ])
    if top_domain == "software" or domain_scores.get("software", 0) >= 2:
        candidates.extend([
            ("Do you enjoy competitive problem solving, backend APIs, app development, or system design more?", "This separates DSA-heavy placement preparation from backend or full-stack project direction."),
            ("Which language or framework do you want to become interview-ready in first?", "This helps convert a broad software interest into a focused roadmap."),
        ])
    if top_domain == "hardware" and "hardware" not in disliked:
        candidates.append(("Do you prefer coding microcontrollers, working with sensors, or building dashboards for device data?", "This narrows embedded, IoT, and edge AI direction."))
    if top_domain == "product" or domain_scores.get("product", 0) >= 2:
        candidates.append(("Do you prefer analyzing business problems, designing product features, talking to users, or presenting insights?", "This separates product analyst, business analyst, and technical PM-style paths."))
    if signals.get("contradictions"):
        candidates.append(("You mentioned both interest and discomfort in one area. Which part attracts you, and which part do you want to avoid?", "This resolves contradictions before the final career recommendation."))
    if academic.get("risk_category") == "High Risk":
        candidates.append(("What academic recovery task must be protected while you build career skills: attendance, GPA, backlog clearing, or assignments?", "Career planning should not ignore current academic risk."))
    candidates.extend([
        ("What skills do you already know well, and which one feels hardest right now?", "This identifies the first skill gap to repair."),
        ("How many focused hours can you realistically give daily for the next 30 days?", "This makes the roadmap executable."),
        ("What kind of project would you be proud to show on GitHub or in an interview?", "This connects learning to portfolio value."),
        ("Is your next goal internship readiness, placement preparation, a strong project, or career clarity?", "The final plan should match the student's immediate target."),
    ])
    for question, reason in candidates:
        if question.lower() not in asked:
            return question, reason
    return ("What is the one outcome you want from the next 90 days: internship, placement prep, strong project, or career clarity?", "This final question helps convert the interview into an action plan.")


def build_report(
    context: dict[str, Any],
    signals: dict[str, Any],
    primary: dict[str, Any],
    secondary: list[dict[str, Any]],
    learning: dict[str, Any],
    confidence: float,
    all_paths: list[dict[str, Any]],
) -> dict[str, Any]:
    academic = context.get("academic_context", {})
    answers = context.get("answers", [])
    student_id = context.get("student_id")
    student_name = context.get("student_name") or "the student"
    primary_path = primary["path"]
    primary_meta = primary["meta"]
    secondary_paths = [
        {
            "path": item["path"],
            "why_it_may_fit": f"Also matches signals around {', '.join(item['meta']['signals'][:3])}.",
            "confidence": round(min(0.82, 0.34 + item["score"] * 0.08), 2),
        }
        for item in secondary
    ]
    career_matrix = _career_fit_matrix(all_paths)
    reasoning_trace = _career_reasoning_trace(context, signals, primary_path)
    confidence_breakdown = _confidence_breakdown(signals, academic, confidence)
    readiness_scores = _readiness_scores(signals, academic, confidence)
    skill_heatmap = _skill_heatmap(primary_meta, signals)
    swot = _swot(signals, academic, primary_path)
    one_year_plan = _one_year_plan(primary_path, primary_meta)
    executive_summary = _executive_summary(student_name, academic, signals, primary_path, confidence, learning)
    academic_concerns = _academic_concerns(academic)
    avoid_note = _avoid_note(primary_path, signals)

    return {
        "executive_summary": executive_summary,
        "student_profile_summary": {
            "name": "" if student_name == "the student" else student_name,
            "student_id": student_id or "",
            "department": academic.get("department", ""),
            "year": academic.get("year", ""),
            "overall_summary": executive_summary["one_paragraph_summary"],
            "confidence_score": confidence,
        },
        "academic_risk_analysis": {
            "risk_category": academic.get("risk_category", "Unknown"),
            "risk_reasoning": _academic_reasoning(academic, primary_path),
            "main_academic_concerns": academic_concerns,
            "protective_factors": _protective_factors(signals),
            "priority_level": "High" if academic.get("risk_category") == "High Risk" else "Medium" if academic.get("risk_category") == "Medium Risk" else "Normal",
        },
        "interest_and_strength_analysis": {
            "dominant_interests": signals.get("interests", []),
            "observed_strengths": signals.get("strengths", []),
            "observed_dislikes": [DOMAIN_LABELS.get(item, item) for item in signals.get("disliked_areas", [])],
            "natural_work_style": _natural_work_style(signals),
            "learning_style": signals.get("learning_style", "practice-first"),
            "motivation_pattern": signals.get("motivation_level", "medium"),
            "repeated_signals": [DOMAIN_LABELS.get(item, item) for item in signals.get("repeated_domains", [])],
        },
        "personality_and_work_style": _personality_and_work_style(signals),
        "career_path_recommendation": {
            "primary_path": primary_path,
            "why_this_path_fits": _why_primary_fits(student_name, academic, signals, primary_path),
            "secondary_paths": secondary_paths,
            "paths_to_avoid_for_now": _paths_to_avoid(primary_path, signals),
        },
        "career_reasoning_trace": reasoning_trace,
        "career_fit_matrix": career_matrix,
        "confidence_breakdown": confidence_breakdown,
        "swot_analysis": swot,
        "skill_gap_analysis": {
            "current_known_skills": signals.get("known_skills", []),
            "missing_core_skills": primary_meta["skills"],
            "skills_to_improve_first": learning["skills_to_improve_first"],
            "skills_not_needed_right_now": skill_heatmap["avoid_for_now"],
        },
        "skill_heatmap": skill_heatmap,
        "readiness_scores": readiness_scores,
        "personalized_skill_roadmap": learning["roadmap"],
        "daily_learning_pattern": learning["daily_learning_pattern"],
        "weekly_plan": learning["weekly_plan"],
        "one_year_growth_plan": one_year_plan,
        "project_recommendations": [
            {
                "project_title": title,
                "difficulty": "Beginner to Intermediate",
                "why_this_project": _project_reason(primary_path, title, signals),
                "skills_used": primary_meta["skills"][:4],
                "deliverables": ["GitHub repository", "README with problem statement", "screenshots or notebook output", "short demo explanation"],
                "github_value": f"Shows practical execution for {primary_path} and gives mentors something concrete to review.",
            }
            for title in primary_meta["projects"][:3]
        ],
        "resource_recommendations": {
            "free_resources": primary_meta["resources"],
            "practice_platforms": _practice_platforms(primary_path),
            "youtube_or_course_suggestions": primary_meta["resources"][:3],
            "documentation_to_read": primary_meta["resources"][-2:],
        },
        "mentor_advice": {
            "short_advice": f"Focus on {primary_path} for the next 90 days, but keep the plan narrow: core basics, one visible project, and weekly review.",
            "hard_truth": avoid_note,
            "encouragement": f"{student_name.title() if student_name != 'the student' else 'The student'} already has enough signal to choose a direction for the next 90 days. The win is execution, not collecting more options.",
            "next_best_action": learning["roadmap"]["next_30_days"][0],
            "what_to_stop_doing": ["Switching domains every week", "Watching tutorials without creating outputs", "Choosing advanced topics before basics"],
            "what_to_continue_doing": ["Reflecting on interests", "Building practical outputs", "Connecting career work to academic recovery"],
        },
        "mistake_warnings": _mistake_warnings(primary_path, signals),
        "interview_and_resume_direction": {
            "resume_positioning": f"Position as an aspiring {primary_path} with evidence from one focused project and measurable learning milestones.",
            "best_project_to_build_next": primary_meta["projects"][0],
            "interview_preparation_focus": primary_meta["interview_focus"],
            "portfolio_message": f"I build practical {primary_path} projects using {', '.join(primary_meta['skills'][:3])} and explain the impact clearly.",
        },
        "parent_or_faculty_summary": _parent_or_faculty_summary(student_name, academic, primary_path, confidence),
        "mentor_review_questions": _mentor_review_questions(primary_path, signals),
        "follow_up_questions": [
            "Which project idea will you commit to this month?",
            "What daily time block can you protect consistently?",
            "Which weak skill should your mentor review first?",
        ],
        "answer_evidence": _answer_evidence(answers),
    }


def _executive_summary(student_name: str, academic: dict[str, Any], signals: dict[str, Any], primary_path: str, confidence: float, learning: dict[str, Any]) -> dict[str, Any]:
    name = student_name.title() if student_name != "the student" else "The student"
    time_text = f"{signals['daily_time_hours']} hours daily" if signals.get("daily_time_hours") else "a consistent daily block"
    department = academic.get("department")
    dept_context = f" Even though the academic department is {department}, the recommendation is based on interview signals and current academic context." if department else ""
    return {
        "one_paragraph_summary": f"{name} shows the strongest fit for {primary_path} because the interview repeatedly points to {', '.join(signals.get('interests', [])[:5]) or 'practical technical exploration'}. The immediate priority is to build fundamentals before chasing advanced topics: follow a 30-day plan around {', '.join(learning['skills_to_improve_first'][:3])}, protect {time_text}, and produce one visible portfolio artifact.{dept_context}",
        "best_fit_path": primary_path,
        "confidence": confidence,
        "immediate_priority": learning["skills_to_improve_first"][0],
        "next_best_action": learning["roadmap"]["next_30_days"][0],
    }


def _academic_reasoning(academic: dict[str, Any], primary_path: str) -> str:
    concerns = _academic_concerns(academic)
    if concerns and concerns != ["No severe academic concern was provided."]:
        return f"Career preparation for {primary_path} should run alongside academic repair: {', '.join(concerns)}. The plan avoids overload by using small daily blocks and one project at a time."
    return f"Academic risk context does not show a severe blocker, so the student can focus on steady {primary_path} preparation while maintaining GPA and attendance."


def _academic_concerns(academic: dict[str, Any]) -> list[str]:
    concerns = []
    if academic.get("current_gpa") is not None and academic.get("current_gpa", 10) < 7:
        concerns.append("GPA consistency")
    if academic.get("attendance_percentage") is not None and academic.get("attendance_percentage", 100) < 75:
        concerns.append("attendance recovery")
    if academic.get("backlogs", 0):
        concerns.append("backlog clearing")
    if academic.get("risk_category") == "High Risk":
        concerns.append("high academic intervention priority")
    return concerns or ["No severe academic concern was provided."]


def _protective_factors(signals: dict[str, Any]) -> list[str]:
    factors = ["willingness to reflect"]
    if signals.get("repeated_domains"):
        factors.append("repeated career interest signals")
    if signals.get("daily_time_hours"):
        factors.append("declared daily study time")
    if signals.get("learning_style") == "project-based":
        factors.append("project-focused learning preference")
    return factors


def _natural_work_style(signals: dict[str, Any]) -> str:
    if signals.get("learning_style") == "project-based":
        return "Hands-on builder who learns best by producing visible outputs."
    if "product" in signals.get("repeated_domains", []):
        return "Product-oriented thinker who may enjoy connecting users, metrics, and communication."
    if "data" in signals.get("repeated_domains", []):
        return "Analytical learner who likes finding patterns and explaining evidence."
    return "Practice-first learner who needs a simple routine and frequent feedback."


def _personality_and_work_style(signals: dict[str, Any]) -> dict[str, Any]:
    repeated = signals.get("repeated_domains", [])
    archetype = "Analyzer" if "data" in repeated else "Builder" if "software" in repeated else "Product thinker" if "product" in repeated else "Explorer"
    consistency = "medium"
    if signals.get("motivation_level") == "high" and signals.get("daily_time_hours"):
        consistency = "manageable if the daily time block is protected"
    return {
        "work_style_archetype": archetype,
        "independence_level": "Can work independently on small milestones, but should review progress weekly with a mentor.",
        "collaboration_style": "Benefits from explaining work to peers or mentors, especially before interviews.",
        "learning_behavior": _natural_work_style(signals),
        "consistency_risk": consistency,
        "attention_or_distraction_risk": "Risk increases if the student switches between too many domains or courses in the same week.",
    }


def _why_primary_fits(student_name: str, academic: dict[str, Any], signals: dict[str, Any], primary_path: str) -> str:
    repeated = [DOMAIN_LABELS.get(item, item) for item in signals.get("repeated_domains", [])]
    dislikes = [DOMAIN_LABELS.get(item, item) for item in signals.get("disliked_areas", [])]
    department = academic.get("department")
    sentence = f"{primary_path} is the strongest fit because the interview shows repeated signals around {', '.join(repeated) if repeated else ', '.join(signals.get('interests', [])[:5]) or 'practical technical learning'}."
    if dislikes:
        sentence += f" The recommendation also respects disliked areas such as {', '.join(dislikes)}, so the plan avoids forcing that direction."
    if department == "Electronics" and "hardware" in signals.get("disliked_areas", []) and ("Data" in primary_path or "Software" in primary_path):
        sentence += " Even though the student is from Electronics, the answers point more toward data/software work than hardware-heavy embedded roles."
    return sentence


def _career_reasoning_trace(context: dict[str, Any], signals: dict[str, Any], final_direction: str) -> dict[str, Any]:
    answers = context.get("answers", [])
    initial_direction = "Exploring"
    for answer in answers:
        stored = answer.get("detected_signals", {})
        if stored.get("recommended_primary_path"):
            initial_direction = stored["recommended_primary_path"]
            break
    strongest = [item.title() for item in signals.get("interests", [])[:6]]
    weak = [DOMAIN_LABELS.get(item, item) for item in signals.get("disliked_areas", [])] or signals.get("weaknesses", [])[:3]
    if initial_direction == "Exploring" or initial_direction == final_direction:
        changed = "No major direction change. The final recommendation matches the strongest repeated interview signals."
    else:
        changed = f"Early answers suggested {initial_direction}, but later answers weighted the evidence more strongly toward {final_direction}."
    confidence_text = "High confidence because answers repeatedly point to one domain." if signals.get("clarity_score", 0) >= 0.75 else "Moderate confidence because some answers are still broad or mixed."
    return {
        "initial_direction": initial_direction,
        "final_direction": final_direction,
        "why_direction_changed": changed,
        "strongest_signals": strongest,
        "weak_signals": weak,
        "confidence_explanation": confidence_text,
    }


def _career_fit_matrix(paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    top_score = max((item["score"] for item in paths), default=1)
    matrix = []
    for item in paths[:5]:
        score = int(max(42, min(96, 52 + (item["score"] / max(top_score, 1)) * 40)))
        matrix.append(
            {
                "career": item["path"],
                "match_score": score,
                "why_it_fits": f"Matches interview signals linked to {', '.join(item['meta']['signals'][:4])}.",
                "risk_or_gap": f"Needs proof through {', '.join(item['meta']['skills'][:3])} before claiming readiness.",
            }
        )
    return matrix


def _confidence_breakdown(signals: dict[str, Any], academic: dict[str, Any], confidence: float) -> dict[str, int]:
    total = int(confidence * 100)
    breakdown = {
        "interest_alignment": 30 if signals.get("repeated_domains") else 22,
        "skill_alignment": 24 if signals.get("known_skills") else 16,
        "project_preference": 20 if signals.get("learning_style") == "project-based" else 14,
        "academic_context": 12 if academic else 8,
        "clarity_of_answers": min(18, max(8, int(signals.get("clarity_score", 0.5) * 18))),
    }
    diff = total - sum(breakdown.values())
    breakdown["clarity_of_answers"] = max(5, breakdown["clarity_of_answers"] + diff)
    return breakdown


def _swot(signals: dict[str, Any], academic: dict[str, Any], primary_path: str) -> dict[str, list[str]]:
    return {
        "strengths": signals.get("strengths", []),
        "weaknesses": signals.get("weaknesses", []),
        "opportunities": [
            f"Build a visible {primary_path} portfolio project.",
            "Use college data or student problems as realistic project stories.",
            "Convert daily learning into GitHub evidence.",
        ],
        "threats": _academic_concerns(academic) + ["domain switching without finishing projects"],
    }


def _skill_heatmap(primary_meta: dict[str, Any], signals: dict[str, Any]) -> dict[str, list[str]]:
    known = set(signals.get("known_skills", []))
    must = [skill for skill in primary_meta["skills"] if skill not in known][:4] or primary_meta["skills"][:3]
    return {
        "must_build_now": must,
        "should_build_next": primary_meta["skills"][2:6],
        "optional_later": primary_meta["roadmap"][3:] or ["advanced specialization"],
        "avoid_for_now": ["advanced deep specialization", "too many courses at once", "tools unrelated to the selected path"],
    }


def _readiness_scores(signals: dict[str, Any], academic: dict[str, Any], confidence: float) -> dict[str, int]:
    gpa = academic.get("current_gpa", 7)
    attendance = academic.get("attendance_percentage", 75)
    academic_score = int(max(35, min(95, (float(gpa) * 7) + (float(attendance) * 0.3)))) if isinstance(gpa, (int, float)) and isinstance(attendance, (int, float)) else 60
    clarity_score = int(signals.get("clarity_score", confidence) * 100)
    project_bonus = 10 if signals.get("learning_style") == "project-based" else 0
    skill_bonus = min(18, len(signals.get("known_skills", [])) * 5)
    return {
        "academic_readiness_score": academic_score,
        "career_clarity_score": clarity_score,
        "internship_readiness_score": max(35, min(88, clarity_score - 8 + project_bonus + skill_bonus)),
        "placement_readiness_score": max(30, min(85, academic_score - 10 + skill_bonus)),
        "project_readiness_score": max(40, min(92, 58 + project_bonus + skill_bonus)),
    }


def _one_year_plan(primary_path: str, primary_meta: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "months_1_3": [f"Build fundamentals for {primary_path}", primary_meta["skills"][0], primary_meta["skills"][1], "publish one mini project"],
        "months_4_6": [primary_meta["projects"][0], "resume update", "mentor review", "basic mock interviews"],
        "months_7_9": [primary_meta["projects"][-1], "internship applications", "interview pattern practice"],
        "months_10_12": ["capstone-level portfolio polishing", "placement-focused revision", "networking and referrals"],
    }


def _project_reason(primary_path: str, title: str, signals: dict[str, Any]) -> str:
    preference = ", ".join(signals.get("project_preferences", [])[:2]) or "visible proof of work"
    return f"{title} fits {primary_path} because it turns {preference} into a concrete portfolio artifact."


def _practice_platforms(primary_path: str) -> list[str]:
    if "Data" in primary_path or "Machine Learning" in primary_path:
        return ["Kaggle", "Mode SQL", "HackerRank SQL"]
    if "Software" in primary_path or "Backend" in primary_path:
        return ["LeetCode", "HackerRank", "GitHub project issues"]
    if "Cybersecurity" in primary_path:
        return ["TryHackMe", "PortSwigger Academy", "OverTheWire"]
    return ["YouTube tutorials", "Official documentation", "Mini project labs"]


def _mistake_warnings(primary_path: str, signals: dict[str, Any]) -> list[str]:
    warnings = ["Do not collect courses without finishing projects.", "Do not switch domains every week."]
    if "Data" in primary_path or "Machine Learning" in primary_path:
        warnings.insert(0, "Do not jump into deep learning before Python data handling, SQL, and statistics basics.")
    if signals.get("disliked_areas"):
        warnings.append("Do not force a disliked area just because it matches the degree branch.")
    return warnings


def _paths_to_avoid(primary_path: str, signals: dict[str, Any]) -> list[dict[str, str]]:
    avoided = [{"path": "Deep specialization too early", "reason": "Build fundamentals and one portfolio project before narrowing too aggressively."}]
    for domain in signals.get("disliked_areas", []):
        avoided.append({"path": DOMAIN_LABELS.get(domain, domain), "reason": "The student explicitly showed low interest or discomfort here."})
    return avoided


def _avoid_note(primary_path: str, signals: dict[str, Any]) -> str:
    if "Data" in primary_path or "Machine Learning" in primary_path:
        return "Do not jump directly into deep learning. First prove Python data handling, SQL, statistics basics, and one readable dashboard or notebook."
    return "Do not mistake planning for progress. Every week should produce a visible output, even if small."


def _parent_or_faculty_summary(student_name: str, academic: dict[str, Any], primary_path: str, confidence: float) -> str:
    name = student_name.title() if student_name != "the student" else "The student"
    risk = academic.get("risk_category", "Unknown")
    return f"{name} currently appears best aligned with {primary_path}. The recommendation confidence is {int(confidence * 100)}%. Academic risk is marked as {risk}, so faculty support should balance academic recovery with one focused career preparation path."


def _mentor_review_questions(primary_path: str, signals: dict[str, Any]) -> list[str]:
    return [
        f"Can the student explain why {primary_path} is preferred over the second-best option?",
        "What exact daily time block will the student protect for the next 30 days?",
        "Which project can be reviewed by a mentor within two weeks?",
        "Which academic concern could block career preparation if ignored?",
        "What evidence should be visible on GitHub or in a resume after 30 days?",
    ]


def _answer_evidence(answers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "question": answer.get("question_text", ""),
            "answer_excerpt": str(answer.get("answer_text", ""))[:220],
        }
        for answer in answers[-5:]
    ]
