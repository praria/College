import json
from pathlib import Path

STUDENT_DATA_FILE = Path(__file__).resolve().parent.parent / "students.json"


def load_students(filename=STUDENT_DATA_FILE):
    """Load student data from the JSON file if it exists."""
    if not Path(filename).exists():
        return []

    with open(filename, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            print("Warning: students.json is empty or invalid. Starting with an empty list.")
    return []
