AVAILABLE_COURSES = ["Mathematics", "Science", "History", "Computer Science", "Art", "English"]


def get_registered_courses(students):
    """Return unique registered courses across all students."""
    return {
        course
        for student in students
        for course in student.get("courses", [])
    }


def view_courses():
    """Display all available courses."""
    print("\n[Placeholder] View Courses")
    for course in AVAILABLE_COURSES:
        print(f"- {course}")


def view_registered_courses(students):
    """Display unique registered courses from all students."""
    print("\n[Placeholder] View Registered Courses")
    registered_courses = get_registered_courses(students)
    if not registered_courses:
        print("No courses registered yet.")
        return

    for course in sorted(registered_courses):
        print(f"- {course}")
