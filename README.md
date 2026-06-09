
## Features

- Structured JSON output
- CSV export
- FastAPI + SearxNG search provider (only accepts google results)

## Run (local, Docker Compose)

1. Build and start services:

```bash
docker compose build --no-cache
docker compose up -d
```

2. Open the app in your browser:

```
http://localhost:8000/
```

Notes:
- The Compose file starts two services: the `api` (FastAPI) and `searxng` (search provider).
- `searxng` is exposed on port `8080`; the API is exposed on `8000`.

## Run (development without Docker)

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Start the backend:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open the frontend at `http://localhost:8000/`.

## Tests

Run tests with:

pytest


