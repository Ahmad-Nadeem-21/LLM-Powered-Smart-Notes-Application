## Frontend – Smart Notes (React)

This is a small React frontend (Vite) for your FastAPI notes backend.

### Features

- **File upload**: Upload a PDF, DOCX, or TXT to the `/upload` endpoint.
- **Notes generation**: Call `/notes/{file_id}` and render the returned notes.
- **Clean UI**: Split layout – upload on the left, notes on the right, dark glassmorphism style.

### Backend assumptions

- Backend runs at `http://localhost:8000`.
- Endpoints:
  - `POST /upload` → `{ file_id, filename, message }`
  - `POST /notes/{file_id}` → `{ file_id, notes, cached }`
  - `GET /file/{file_id}` → raw file

If your backend is on a different origin, set:

```bash
VITE_API_BASE_URL="http://your-backend-host:port"
```

### Install & run

```bash
cd frontend
npm install
npm run dev
```

Then open the URL Vite prints (by default `http://localhost:5173`).


