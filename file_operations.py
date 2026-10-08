import csv
import io
import json


def students_csv_content(students):
    """Return student data formatted as CSV text."""
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["id", "name", "age", "courses"])
    for student in students:
        writer.writerow([
            student.get("id", ""),
            student.get("name", ""),
            student.get("age", ""),
            ", ".join(student.get("courses", [])),
        ])
    return output.getvalue()


def save_students_json(students, filename="students.json"):
    """Save the current student list to a JSON file."""
    print(f"\n[Placeholder] Save Students to {filename}")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=2)
    print(f"Student data saved to {filename}.")


def export_students_csv(students, filename="students.csv"):
    """Export student data to a CSV file."""
    print(f"\n[Placeholder] Export CSV to {filename}")
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(students_csv_content(students))
    print(f"Students exported to {filename}.")
