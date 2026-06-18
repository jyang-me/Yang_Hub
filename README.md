# My Blog

Personal website scaffold with Vue 3, Vite, Django REST Framework, and SQLite.

## Backend

```powershell
.\.venv\Scripts\activate
cd backend
python manage.py runserver
```

API base URL:

```text
http://127.0.0.1:8000/api/
```

Available resources:

- `GET /api/categories/`
- `GET /api/tags/`
- `GET /api/posts/`
- `GET /api/posts/<slug>/`
- `GET /api/projects/`
- `GET /api/projects/<slug>/`
- `POST /api/messages/`

Create an admin user:

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py createsuperuser
```

## Frontend

```powershell
cd frontend
npm.cmd run dev
```

Vite dev server:

```text
http://localhost:5173/
```

## Notes

- Blog post content is stored as Markdown text in the backend.
- The Vue frontend should render Markdown using a client-side library such as `markdown-it` or `marked`.
- Uploaded media is stored in `backend/media/` during local development.
