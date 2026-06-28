from __future__ import annotations

from typing import Any


CAREER_PATHS: dict[str, dict[str, Any]] = {
    "Data Scientist": {
        "signals": ["python", "math", "maths", "statistics", "ml", "machine learning", "data", "pandas"],
        "skills": ["Python", "Pandas", "SQL", "Statistics", "Machine Learning", "Visualization"],
        "roadmap": ["Python data handling", "SQL basics", "Statistics", "ML fundamentals", "Portfolio notebooks"],
        "projects": ["Student performance analytics notebook", "Placement prediction dashboard"],
        "interview_focus": ["Python", "SQL", "statistics basics", "ML project explanation"],
        "resources": ["Kaggle Learn", "Pandas documentation", "StatQuest", "scikit-learn docs"],
    },
    "Data Analyst": {
        "signals": ["data", "excel", "power bi", "sql", "analytics", "dashboard", "visualization"],
        "skills": ["SQL", "Excel", "Power BI", "Python basics", "Storytelling"],
        "roadmap": ["SQL queries", "Excel analysis", "Power BI dashboards", "case studies"],
        "projects": ["College attendance dashboard", "Department performance BI report"],
        "interview_focus": ["SQL", "dashboard explanation", "business metrics"],
        "resources": ["Mode SQL tutorial", "Microsoft Power BI Learn", "Kaggle datasets"],
    },
    "Machine Learning Engineer": {
        "signals": ["ml", "machine learning", "model", "ai", "python", "deep learning"],
        "skills": ["Python", "Scikit-learn", "ML pipelines", "APIs", "Model evaluation"],
        "roadmap": ["Python", "ML fundamentals", "model serving", "MLOps basics"],
        "projects": ["Explainable ML API", "Recommendation engine"],
        "interview_focus": ["ML concepts", "model metrics", "deployment basics"],
        "resources": ["Google ML Crash Course", "scikit-learn docs", "FastAPI docs"],
    },
    "Software Engineer": {
        "signals": ["coding", "dsa", "java", "backend", "api", "apps", "systems", "debugging"],
        "skills": ["DSA", "Java or Python", "APIs", "Databases", "Git", "System basics"],
        "roadmap": ["DSA", "backend APIs", "database design", "one full-stack project"],
        "projects": ["Student management API", "Task tracker with auth later"],
        "interview_focus": ["DSA", "OOP", "DBMS", "API project"],
        "resources": ["NeetCode", "LeetCode", "FastAPI docs", "PostgreSQL tutorial"],
    },
    "Backend Developer": {
        "signals": ["backend", "api", "database", "server", "fastapi", "django"],
        "skills": ["Python/Java", "REST APIs", "SQL", "Caching", "Testing"],
        "roadmap": ["API basics", "database models", "testing", "deployment concepts"],
        "projects": ["Mentor API backend", "CSV analytics API"],
        "interview_focus": ["REST", "SQL", "auth concepts", "testing"],
        "resources": ["FastAPI docs", "SQLBolt", "Real Python"],
    },
    "Embedded Systems Engineer": {
        "signals": ["circuits", "sensors", "arduino", "electronics", "hardware", "robotics", "embedded"],
        "skills": ["C", "Embedded C", "Sensors", "Microcontrollers", "IoT basics"],
        "roadmap": ["C basics", "Arduino projects", "sensor integration", "IoT dashboard"],
        "projects": ["Attendance sensor prototype", "IoT environment monitor"],
        "interview_focus": ["C", "microcontrollers", "basic electronics"],
        "resources": ["Arduino docs", "Embedded C tutorials", "ESP32 docs"],
    },
    "IoT / Edge AI Engineer": {
        "signals": ["iot", "edge", "sensors", "hardware", "ai on device", "esp32"],
        "skills": ["Sensors", "Python/C", "IoT protocols", "Edge inference"],
        "roadmap": ["IoT basics", "sensor data logging", "tiny ML basics"],
        "projects": ["Sensor analytics dashboard", "Edge anomaly detector"],
        "interview_focus": ["IoT architecture", "sensor interfacing", "data flow"],
        "resources": ["ESP32 docs", "Edge Impulse", "Arduino IoT"],
    },
    "Product Analyst": {
        "signals": ["product", "users", "planning", "analytics", "business", "communication"],
        "skills": ["SQL", "Product metrics", "User research", "Dashboards", "Communication"],
        "roadmap": ["SQL", "metrics", "case studies", "dashboard storytelling"],
        "projects": ["Student success metrics dashboard", "Feature adoption analysis"],
        "interview_focus": ["product sense", "metrics", "SQL"],
        "resources": ["Lenny's Newsletter free posts", "Mode SQL", "Product case libraries"],
    },
    "Business Analyst": {
        "signals": ["business", "communication", "requirements", "presentation", "stakeholders"],
        "skills": ["Excel", "SQL basics", "Requirements", "Documentation", "Presentation"],
        "roadmap": ["Excel", "SQL basics", "requirements documents", "case studies"],
        "projects": ["Academic process improvement report", "Placement readiness analysis"],
        "interview_focus": ["case thinking", "communication", "basic analytics"],
        "resources": ["BA templates", "Excel practice", "SQL basics"],
    },
    "Technical Product Manager": {
        "signals": ["leadership", "planning", "product", "users", "features", "roadmap"],
        "skills": ["Product thinking", "Technical basics", "Communication", "Prioritization"],
        "roadmap": ["Build projects", "write PRDs", "learn metrics", "practice product cases"],
        "projects": ["SmartEdu feature PRD", "Analytics dashboard roadmap"],
        "interview_focus": ["product sense", "execution", "technical tradeoffs"],
        "resources": ["Exponent PM videos", "Product School free resources"],
    },
    "Cybersecurity Analyst": {
        "signals": ["security", "hacking", "networks", "cyber", "linux"],
        "skills": ["Networking", "Linux", "Web security", "Python scripting"],
        "roadmap": ["Networking", "Linux", "OWASP basics", "CTF practice"],
        "projects": ["Secure login audit", "Network scanner lab"],
        "interview_focus": ["networks", "OWASP", "Linux"],
        "resources": ["TryHackMe", "OWASP WebGoat", "PortSwigger Academy"],
    },
    "Frontend Developer": {
        "signals": ["frontend", "website", "ui", "react", "design", "creative"],
        "skills": ["HTML", "CSS", "JavaScript", "React", "UI basics"],
        "roadmap": ["HTML/CSS", "JS", "React", "portfolio UI"],
        "projects": ["Student dashboard UI", "Portfolio site"],
        "interview_focus": ["JS basics", "components", "CSS layout"],
        "resources": ["MDN", "React docs", "Frontend Mentor"],
    },
    "UI/UX + Product Design": {
        "signals": ["design", "ui", "ux", "figma", "users", "creative"],
        "skills": ["Figma", "User research", "Wireframing", "Product thinking"],
        "roadmap": ["Figma basics", "redesign case study", "usability thinking"],
        "projects": ["SmartEdu dashboard redesign case study", "Student app prototype"],
        "interview_focus": ["design process", "case studies", "user empathy"],
        "resources": ["Figma Learn", "Nielsen Norman articles", "Mobbin examples"],
    },
}


def score_paths(signals: dict[str, Any]) -> list[dict[str, Any]]:
    text = " ".join(
        str(item).lower()
        for key in ["interests", "strengths", "career_hints", "known_skills", "project_preferences", "career_goal"]
        for item in signals.get(key, [])
    )
    signal_counts = signals.get("signal_counts", {})
    disliked_areas = set(signals.get("disliked_areas", []))
    scored = []
    for path, meta in CAREER_PATHS.items():
        score = sum(1 for signal in meta["signals"] if signal in text)
        for signal in meta["signals"]:
            score += int(signal_counts.get(signal, 0))
        if "hardware" in disliked_areas and path in {"Embedded Systems Engineer", "IoT / Edge AI Engineer"}:
            score -= 3
        if "data" in signals.get("repeated_domains", []) and path in {"Data Scientist", "Data Analyst", "Machine Learning Engineer"}:
            score += 2
        if "software" in signals.get("repeated_domains", []) and path in {"Software Engineer", "Backend Developer"}:
            score += 2
        if score > 0:
            scored.append({"path": path, "score": score, "meta": meta})
    fallback_order = ["Data Scientist", "Data Analyst", "Software Engineer", "Backend Developer", "Product Analyst"]
    existing = {item["path"] for item in scored}
    for path in fallback_order:
        if len(scored) >= 5:
            break
        if path not in existing:
            scored.append({"path": path, "score": 1, "meta": CAREER_PATHS[path]})
    return sorted(scored, key=lambda item: item["score"], reverse=True)
