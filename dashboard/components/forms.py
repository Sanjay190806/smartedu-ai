from __future__ import annotations

import streamlit as st

from dashboard.utils.sample_payloads import HIGH_RISK_SAMPLE, LOW_RISK_SAMPLE, MEDIUM_RISK_SAMPLE


def sample_payload_buttons() -> None:
    col1, col2, col3 = st.columns(3)
    if col1.button("Load High Risk Sample", use_container_width=True):
        st.session_state.active_sample_payload = HIGH_RISK_SAMPLE.copy()
    if col2.button("Load Medium Risk Sample", use_container_width=True):
        st.session_state.active_sample_payload = MEDIUM_RISK_SAMPLE.copy()
    if col3.button("Load Low Risk Sample", use_container_width=True):
        st.session_state.active_sample_payload = LOW_RISK_SAMPLE.copy()


def student_prediction_form() -> dict:
    defaults = st.session_state.get("active_sample_payload") or MEDIUM_RISK_SAMPLE
    with st.form("student_prediction_form"):
        st.subheader("Student Identity")
        c1, c2, c3 = st.columns(3)
        student_id = c1.text_input("Student ID", value=defaults["student_id"])
        name = c2.text_input("Name", value=defaults["name"])
        department = c3.selectbox(
            "Department",
            ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Data Science"],
            index=["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Data Science"].index(defaults["department"]),
        )
        c4, c5, c6 = st.columns(3)
        year = c4.number_input("Year", 1, 4, int(defaults["year"]))
        semester = c5.number_input("Semester", 1, 8, int(defaults["semester"]))
        gender = c6.selectbox("Gender", ["Female", "Male", "Non-binary"], index=["Female", "Male", "Non-binary"].index(defaults["gender"]))

        st.subheader("Academic Performance")
        a1, a2, a3 = st.columns(3)
        attendance = a1.slider("Attendance %", 0, 100, int(defaults["attendance_percentage"]))
        internal_marks = a2.slider("Internal Marks Average", 0, 100, int(defaults["internal_marks_average"]))
        assignment_rate = a3.slider("Assignment Completion %", 0, 100, int(defaults["assignment_completion_rate"]))
        a4, a5, a6 = st.columns(3)
        quiz_average = a4.slider("Quiz Average", 0, 100, int(defaults["quiz_average"]))
        previous_gpa = a5.number_input("Previous Semester GPA", 0.0, 10.0, float(defaults["previous_semester_gpa"]), step=0.1)
        current_gpa = a6.number_input("Current GPA", 0.0, 10.0, float(defaults["current_gpa"]), step=0.1)
        a7, a8, a9 = st.columns(3)
        study_hours = a7.number_input("Study Hours/Week", 0.0, 80.0, float(defaults["study_hours_per_week"]), step=0.5)
        backlogs = a8.number_input("Backlogs", 0, 20, int(defaults["backlogs"]))
        late_submissions = a9.number_input("Late Submissions", 0, 50, int(defaults["late_submissions"]))
        participation = st.slider("Participation Score", 0, 100, int(defaults["participation_score"]))

        st.subheader("Subject Scores")
        s1, s2, s3, s4, s5 = st.columns(5)
        math = s1.slider("Math", 0, 100, int(defaults["subject_math_score"]))
        programming = s2.slider("Programming", 0, 100, int(defaults["subject_programming_score"]))
        electronics = s3.slider("Electronics", 0, 100, int(defaults["subject_electronics_score"]))
        communication = s4.slider("Communication", 0, 100, int(defaults["subject_communication_score"]))
        lab = s5.slider("Lab", 0, 100, int(defaults["subject_lab_score"]))

        st.subheader("Engagement and Wellbeing")
        e1, e2, e3, e4 = st.columns(4)
        library = e1.number_input("Library Hours", 0.0, 80.0, float(defaults["library_usage_hours"]), step=0.5)
        lms = e2.number_input("LMS Logins/Week", 0, 100, int(defaults["lms_login_frequency"]))
        parent_meetings = e3.number_input("Parent Meetings", 0, 20, int(defaults["parent_meeting_count"]))
        mentor_meetings = e4.number_input("Mentor Meetings", 0, 20, int(defaults["mentor_meeting_count"]))
        e5, e6, e7, e8 = st.columns(4)
        extracurricular = e5.number_input("Extracurricular Hours", 0.0, 80.0, float(defaults["extracurricular_hours"]), step=0.5)
        stress = e6.slider("Stress Level", 1, 10, int(defaults["stress_level"]))
        sleep = e7.number_input("Sleep Hours", 0.0, 12.0, float(defaults["sleep_hours"]), step=0.1)
        internet = e8.selectbox("Internet Access", ["Yes", "No"], index=0 if defaults["internet_access"] == "Yes" else 1)

        submitted = st.form_submit_button("Predict Risk", use_container_width=True)

    payload = {
        "student_id": student_id,
        "name": name,
        "department": department,
        "year": year,
        "semester": semester,
        "gender": gender,
        "attendance_percentage": attendance,
        "internal_marks_average": internal_marks,
        "assignment_completion_rate": assignment_rate,
        "quiz_average": quiz_average,
        "previous_semester_gpa": previous_gpa,
        "current_gpa": current_gpa,
        "study_hours_per_week": study_hours,
        "backlogs": backlogs,
        "late_submissions": late_submissions,
        "participation_score": participation,
        "subject_math_score": math,
        "subject_programming_score": programming,
        "subject_electronics_score": electronics,
        "subject_communication_score": communication,
        "subject_lab_score": lab,
        "library_usage_hours": library,
        "lms_login_frequency": lms,
        "parent_meeting_count": parent_meetings,
        "mentor_meeting_count": mentor_meetings,
        "extracurricular_hours": extracurricular,
        "stress_level": stress,
        "sleep_hours": sleep,
        "internet_access": internet,
    }
    return {"submitted": submitted, "payload": payload}
