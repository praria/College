from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field

from .course_operations import AVAILABLE_COURSES, get_registered_courses
from .data_store import STUDENT_DATA_FILE, load_students
from .file_operations import students_csv_content, write_students_json
from .student_operations import add_student, find_students

app = FastAPI(title="College Student Management API", version="1.0.0")
students = load_students()


class StudentCreate(BaseModel):
    name: str
    age: int
    courses: list[str] = Field(default_factory=list)


@app.get("/students")
def list_students():
    return students


@app.post("/students", status_code=201)
def create_student(student_data: StudentCreate):
    succeeded, message = add_student(
        students,
        student_data.name,
        student_data.age,
        student_data.courses,
    )
    if not succeeded:
        raise HTTPException(status_code=422, detail=message)

    try:
        write_students_json(students, STUDENT_DATA_FILE)
    except OSError as error:
        students.pop()
        raise HTTPException(status_code=500, detail="Could not save student data.") from error

    return {"message": message, "student": students[-1]}


@app.get("/students/search")
def search_students(name: Annotated[str, Query(min_length=1)]):
    return find_students(students, name)


@app.get("/students/eligibility")
def check_student_eligibility(
    name: Annotated[str | None, Query(min_length=1)] = None,
    student_id: int | None = None,
):
    if student_id is not None:
        matches = [student for student in students if student.get("id") == student_id]
    elif name is not None:
        matches = find_students(students, name)
    else:
        raise HTTPException(
            status_code=422,
            detail="Provide either a student name or student ID.",
        )

    if not matches:
        if student_id is not None:
            raise HTTPException(
                status_code=404,
                detail=f"No student with ID {student_id} was found.",
            )
        raise HTTPException(status_code=404, detail=f"No student named '{name}' was found.")

    student = matches[0]
    return {
        "id": student.get("id"),
        "name": student.get("name"),
        "eligible": student.get("age", 0) >= 18,
    }


@app.get("/courses")
def list_courses():
    return AVAILABLE_COURSES


@app.get("/courses/registered")
def list_registered_courses():
    return sorted(get_registered_courses(students))


@app.post("/students/save")
def save_students():
    try:
        write_students_json(students, STUDENT_DATA_FILE)
    except OSError as error:
        raise HTTPException(status_code=500, detail="Could not save student data.") from error
    return {"message": "Student data saved."}


@app.get("/students/export/csv")
def export_students():
    return Response(
        content=students_csv_content(students),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="students.csv"'},
    )
