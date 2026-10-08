import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT_SECONDS = 10


def api_request(method, path, **kwargs):
    """Send a request to the backend API and display errors in the UI."""
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT_SECONDS,
            **kwargs,
        )
    except requests.RequestException as error:
        st.error(f"Could not connect to the backend API at {API_BASE_URL}: {error}")
        st.stop()

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        st.error(f"API request failed ({response.status_code}): {detail}")
        st.stop()

    return response


st.set_page_config(page_title="Student Management System", page_icon="🎓")
st.title("Student Management System")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Register Student",
        "View Students",
        "Search Student",
        "Check Eligibility",
        "View Courses",
        "View Registered Courses",
        "Save & Export",
    ],
)

if page == "Dashboard":
    students = api_request("GET", "/students").json()
    available_courses = api_request("GET", "/courses").json()
    registered_courses = api_request("GET", "/courses/registered").json()

    st.write("Manage student records and course registrations.")
    first_metric, second_metric, third_metric, fourth_metric = st.columns(4)
    first_metric.metric("Students", len(students))
    second_metric.metric("Available courses", len(available_courses))
    second_metric.metric("Registered courses", len(registered_courses))
    third_metric.metric(
        "Eligible students (18+)",
        sum(student.get("age", 0) >= 18 for student in students),
    )
    fourth_metric.metric("Courses per student", "Up to 3")

elif page == "Register Student":
    st.subheader("Register a student")
    available_courses = api_request("GET", "/courses").json()
    with st.form("register_student_form"):
        name = st.text_input("Student name")
        age = st.number_input("Age (minimum 16)", min_value=0, step=1)
        courses = st.multiselect(
            "Courses (up to 3)",
            options=available_courses,
            max_selections=3,
        )
        submitted = st.form_submit_button("Register student")

    if submitted:
        response = api_request(
            "POST",
            "/students",
            json={"name": name, "age": age, "courses": courses},
        )
        st.success(response.json()["message"])

elif page == "View Students":
    st.subheader("Registered students")
    students = api_request("GET", "/students").json()
    if students:
        student_rows = [
            {
                **student,
                "courses": ", ".join(student.get("courses", [])),
            }
            for student in students
        ]
        st.dataframe(student_rows, width="stretch", hide_index=True)
    else:
        st.info("No students registered yet.")

elif page == "Search Student":
    st.subheader("Search students")
    with st.form("search_student_form"):
        search_name = st.text_input("Student name")
        submitted = st.form_submit_button("Search")

    if submitted and search_name.strip():
        matches = api_request(
            "GET",
            "/students/search",
            params={"name": search_name.strip()},
        ).json()
        if matches:
            st.dataframe(matches, width="stretch", hide_index=True)
        else:
            st.info(f"No student named '{search_name}' was found.")

elif page == "Check Eligibility":
    st.subheader("Check eligibility")
    students = api_request("GET", "/students").json()
    if students:
        selected_student = st.selectbox(
            "Student",
            students,
            format_func=lambda student: (
                f"{student.get('name', '')} (ID: {student.get('id', '')})"
            ),
        )
        eligibility = api_request(
            "GET",
            "/students/eligibility",
            params={"student_id": selected_student["id"]},
        ).json()
        if eligibility["eligible"]:
            st.success(
                f"{eligibility['name']} is eligible (age 18 or older)."
            )
        else:
            st.warning(
                f"{eligibility['name']} is not eligible (must be at least 18)."
            )
    else:
        st.info("Register a student before checking eligibility.")

elif page == "View Courses":
    st.subheader("Available courses")
    available_courses = api_request("GET", "/courses").json()
    for course in available_courses:
        st.write(f"- {course}")

elif page == "View Registered Courses":
    st.subheader("Registered courses")
    registered_courses = api_request("GET", "/courses/registered").json()
    if registered_courses:
        for course in registered_courses:
            st.write(f"- {course}")
    else:
        st.info("No courses registered yet.")

elif page == "Save & Export":
    st.subheader("Save and export student data")
    if st.button("Save students to JSON"):
        response = api_request("POST", "/students/save")
        st.success(response.json()["message"])

    csv_response = api_request("GET", "/students/export/csv")
    st.download_button(
        "Download students as CSV",
        data=csv_response.content,
        file_name="students.csv",
        mime="text/csv",
    )
