# College Student Management

## Run the Streamlit app

```bash
streamlit run app.py
```

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
- `GET /courses` — list available courses
- `GET /courses/registered` — list unique registered courses
- `POST /students/save` — explicitly save the current API student list
- `GET /students/export/csv` — download student data as CSV

The Streamlit app retains its existing explicit-save behavior. Its student operations
and the CLI are in the `backend` package; `main.py` remains the CLI entry point.