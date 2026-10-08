import json
import os
from pathlib import Path

from course_operations import view_courses, view_registered_courses
from file_operations import export_students_csv, save_students_json
from student_operations import check_eligibility, register_student, search_student, view_students

MENU_CHOICES = tuple(str(choice) for choice in range(1, 10))
STUDENT_DATA_FILE = Path(__file__).with_name("students.json")


def load_students(filename=STUDENT_DATA_FILE):
    """Load student data from the JSON file if it exists."""
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            print("Warning: students.json is empty or invalid. Starting with an empty list.")
    return []


def display_menu():
    print("\n=== Student Management System ===")
    print("1. Register Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Check Eligibility")
    print("5. View Courses")
    print("6. View Registered Courses")
    print("7. Save Students")
    print("8. Export CSV")
    print("9. Exit")


def get_validated_choice(prompt, valid_choices):
    """Prompt until the input matches one of the allowed choices."""
    choices_text = ", ".join(valid_choices)
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please enter one of: {choices_text}.")


def main():
    students = load_students()

    while True:
        display_menu()
        choice = get_validated_choice("Enter your choice (1-9): ", MENU_CHOICES)

        if choice == "1":
            register_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            name = input("Enter student name to search: ").strip()
            search_student(students, name)
        elif choice == "4":
            check_eligibility(students)
        elif choice == "5":
            view_courses()
        elif choice == "6":
            view_registered_courses(students)
        elif choice == "7":
            save_students_json(students, STUDENT_DATA_FILE)
        elif choice == "8":
            export_students_csv(students, STUDENT_DATA_FILE.with_name("students.csv"))
        elif choice == "9":
            print("\nSaving data before exit...")
            save_students_json(students, STUDENT_DATA_FILE)
            print("Program closed.")
            break


if __name__ == "__main__":
    main()
