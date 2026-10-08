# College Student Management

A student management application with a Streamlit interface and a FastAPI backend. It supports registering and searching students, checking eligibility, viewing course registrations, and saving or exporting student data.

## Run the Streamlit app

Start the API in one terminal:

```bash
collegevenv/bin/python -m uvicorn backend.api:app --reload
```

Then start the frontend from the project directory in another terminal:

```bash
collegevenv/bin/streamlit run frontend/app.py
```

The frontend connects to `http://127.0.0.1:8000` by default. Set the
`API_BASE_URL` environment variable to use a different API address.

## Run the command-line interface

```bash
python main.py
```

## Run the API

Install the requirements and start the API from this directory:

```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.api:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at
`http://127.0.0.1:8000/docs`.

### Endpoints

- `GET /students` — list students
- `POST /students` — register a student; successful registrations are saved to `students.json`
- `GET /students/search?name=...` — find matching students
- `GET /students/eligibility?name=...` — check the first matching student's eligibility
  (`student_id=...` can target a specific student)
- `GET /courses` — list available courses
- `GET /courses/registered` — list unique registered courses
- `POST /students/save` — explicitly save the current API student list
- `GET /students/export/csv` — download student data as CSV

The Streamlit frontend communicates with the API; it does not access backend
modules or student data files directly. Student registrations made from the
frontend are saved immediately by the API. The CLI remains available through
`main.py`.