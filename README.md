# Secure Student Records API

A FastAPI application for registering users, signing in, and managing student records. User passwords are stored as hashes, API access uses bearer tokens, and only admins can create, update, or delete student records.

## Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/)

The project needs FastAPI, Uvicorn, SQLAlchemy, Pydantic Settings, `python-jose`, `pwdlib` with Argon2 support, `python-multipart`, and `email-validator` installed in its virtual environment.

## Configure

Create a file named `.env` in the project root (next to the `app` folder), containing:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
```

Keep this secret private. The SQLite database is stored in `students.db` in the current working directory and its tables are created when the app starts.

## Run

From the project root, start the development server:

```powershell
uv run uvicorn app.main:app --reload
```

Open the interactive API page at <http://127.0.0.1:8000/docs>. The root URL, <http://127.0.0.1:8000/>, returns a message confirming the API is running.

## Authentication and roles

1. Use `POST /auth/register` to create an account. New accounts have the `student` role.
2. Use `POST /auth/login` with the account username and password. Login accepts form fields and returns a bearer access token.
3. In `/docs`, click **Authorize** and enter the access token. Protected student endpoints require it.

Registered accounts cannot grant themselves admin access. For local development only, an existing account can be promoted by updating its role in `students.db`. Run this from the project root, replacing `YOUR_USERNAME` with the exact username returned by the query:

```powershell
uv run python -c "import sqlite3; c=sqlite3.connect('students.db'); print(c.execute('SELECT username, role FROM users').fetchall()); c.close()"
uv run python -c "import sqlite3; c=sqlite3.connect('students.db'); r=c.execute('UPDATE users SET role=? WHERE username=?', ('admin', 'YOUR_USERNAME')); c.commit(); print('Updated accounts:', r.rowcount); c.close()"
```

The update should print `Updated accounts: 1`. Log in again after changing the role and authorize with the newly issued token. Do not expose database access or an admin promotion mechanism to public users.

## Endpoints

| Method | Path | Access | Purpose |
| --- | --- | --- | --- |
| `GET` | `/` | Public | Check that the API is running |
| `POST` | `/auth/register` | Public | Register a student account |
| `POST` | `/auth/login` | Public | Sign in and receive a bearer token |
| `GET` | `/students/` | Authenticated | List student records |
| `GET` | `/students/{student_id}` | Authenticated | Get one student record |
| `POST` | `/students/` | Admin | Create a student record |
| `PUT` | `/students/{student_id}` | Admin | Replace a student record's fields |
| `DELETE` | `/students/{student_id}` | Admin | Delete a student record |

Student records use this JSON shape for create and update requests:

```json
{
  "name": "Alex Rivera",
  "email": "alex@example.com",
  "course": "Computer Science",
  "year": 1
}
```

The year must be between 1 and 6. Student emails must be valid and unique. Missing student IDs return `404`; requests without a valid token return `401`; authenticated non-admins attempting admin-only operations receive `403`.
