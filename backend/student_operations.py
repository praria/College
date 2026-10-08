from .course_operations import AVAILABLE_COURSES


def add_student(students, name, age, courses):
    """Validate and add a student, returning the operation result and message."""
    name = name.strip()
    if not name:
        return False, "Student name cannot be empty."

    if age < 16:
        return False, "Student age must be at least 16."

    invalid_courses = [course for course in courses if course not in AVAILABLE_COURSES]
    if invalid_courses:
        return False, f"Invalid course selection. Available courses: {', '.join(AVAILABLE_COURSES)}."

    if len(courses) > 3:
        return False, "A student cannot register more than 3 courses."

    student = {
        "id": len(students) + 1,
        "name": name,
        "age": age,
        "courses": courses,
    }
    students.append(student)
    return True, f"Student '{name}' registered successfully."


def find_students(students, name):
    """Return students whose names match, ignoring letter case."""
    normalized_name = name.strip().casefold()
    return [
        student
        for student in students
        if student.get("name", "").casefold() == normalized_name
    ]


def register_student(students):
    """Add a new student to the in-memory list."""
    print("\n[Placeholder] Register Student")

    name = input("Enter student name: ").strip()

    age_input = input("Enter student age: ").strip()
    try:
        age = int(age_input)
    except ValueError:
        print("Invalid age. Age must be a number.")
        return students

    courses_input = input("Enter courses (comma-separated): ").strip()
    courses = [course.strip() for course in courses_input.split(",") if course.strip()] if courses_input else []

    _, message = add_student(students, name, age, courses)
    print(message)
    return students


def view_students(students):
    """Display all students."""
    print("\n[Placeholder] View Students")
    if not students:
        print("No students registered yet.")
        return

    for student in students:
        print(f"ID: {student.get('id')} | Name: {student.get('name')} | Age: {student.get('age')} | Courses: {student.get('courses', [])}")


def search_student(students, name):
    """Search student by name and display result."""
    print(f"\n[Placeholder] Search Student: {name}")
    if not students:
        print("No students available.")
        return

    matches = find_students(students, name)
    if matches:
        print(f"Student found: {matches[0]}")
    else:
        print(f"No student named '{name}' was found.")


def check_eligibility(students):
    """Check if a student is eligible (age >= 18)."""
    print("\n[Placeholder] Check Eligibility")
    if not students:
        print("No students registered yet.")
        return

    name = input("Enter student name to check eligibility: ").strip()
    for student in students:
        if student.get("name", "").lower() == name.lower():
            status = "Eligible" if student.get("age", 0) >= 18 else "Not Eligible"
            print(f"{student.get('name')} is {status}.")
            return

    print(f"No student named '{name}' was found.")
