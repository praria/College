import streamlit as st

from course_operations import AVAILABLE_COURSES, get_registered_courses
from file_operations import save_students_json, students_csv_content
from main import STUDENT_DATA_FILE, load_students
from student_operations import add_student, find_students


st.set_page_config(page_title="Student Management System", page_icon="🎓")

if "students" not in st.session_state:
    st.session_state.students = load_students()
if "students_dirty" not in st.session_state:
    st.session_state.students_dirty = False

students = st.session_state.students

st.title("Student Management System")
if st.session_state.students_dirty:
    st.warning("You have unsaved changes. Save them from the Save & Export page.")

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
    st.write("Manage student records and course registrations.")
    first_metric, second_metric, third_metric, fourth_metric = st.columns(4)
    first_metric.metric("Students", len(students))
    second_metric.metric("Available courses", len(AVAILABLE_COURSES))
    second_metric.metric("Registered courses", len(get_registered_courses(students)))
    third_metric.metric(
        "Eligible students (18+)",
        sum(student.get("age", 0) >= 18 for student in students),
    )
    fourth_metric.metric("Courses per student", "Up to 3")

elif page == "Register Student":
    st.subheader("Register a student")
    with st.form("register_student_form"):
        name = st.text_input("Student name")
        age = st.number_input("Age (minimum 16)", min_value=0, step=1)
        courses = st.multiselect(
            "Courses (up to 3)",
            options=AVAILABLE_COURSES,
            max_selections=3,
        )
        submitted = st.form_submit_button("Register student")

    if submitted:
        succeeded, message = add_student(students, name, age, courses)
        if succeeded:
            st.session_state.students_dirty = True
            st.success(message)
        else:
            st.error(message)

elif page == "View Students":
    st.subheader("Registered students")
    if students:
        student_rows = [
            {
                **student,
                "courses": ", ".join(student.get("courses", [])),
            }
            for student in students
        ]
        st.dataframe(student_rows, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")

elif page == "Search Student":
    st.subheader("Search students")
    search_name = st.text_input("Student name")
    if search_name.strip():
        matches = find_students(students, search_name)
        if matches:
            st.dataframe(matches, use_container_width=True, hide_index=True)
        else:
            st.info(f"No student named '{search_name}' was found.")

elif page == "Check Eligibility":
    st.subheader("Check eligibility")
    if students:
        selected_student = st.selectbox(
            "Student",
            students,
            format_func=lambda student: (
                f"{student.get('name', '')} (ID: {student.get('id', '')})"
            ),
        )
        if selected_student.get("age", 0) >= 18:
            st.success(
                f"{selected_student.get('name')} is eligible (age 18 or older)."
            )
        else:
            st.warning(
                f"{selected_student.get('name')} is not eligible (must be at least 18)."
            )
    else:
        st.info("Register a student before checking eligibility.")

elif page == "View Courses":
    st.subheader("Available courses")
    for course in AVAILABLE_COURSES:
        st.write(f"- {course}")

elif page == "View Registered Courses":
    st.subheader("Registered courses")
    registered_courses = sorted(get_registered_courses(students))
    if registered_courses:
        for course in registered_courses:
            st.write(f"- {course}")
    else:
        st.info("No courses registered yet.")

elif page == "Save & Export":
    st.subheader("Save and export student data")
    if st.button("Save students to JSON"):
        try:
            save_students_json(students, STUDENT_DATA_FILE)
        except OSError as error:
            st.error(f"Could not save student data: {error}")
        else:
            st.session_state.students_dirty = False
            st.success(f"Student data saved to {STUDENT_DATA_FILE.name}.")

    st.download_button(
        "Download students as CSV",
        data=students_csv_content(students),
        file_name="students.csv",
        mime="text/csv",
    )
