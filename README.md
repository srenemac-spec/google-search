
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

## Deployment to Render (recommended)

This repo now includes a Render manifest and a dedicated SearxNG Dockerfile to ensure `settings.yml` is always included.

### Recommended Render setup

1. Push this repository to GitHub (already done).
2. In Render, connect this repo and use the provided `render.yaml` manifest.
3. The manifest defines two services:
   - `google-search-api` — built with the repo `Dockerfile`.
   - `google-search-searxng` — built with `Dockerfile.searxng` and copies `settings.yml` into the container.
4. Set the environment variable for the `api` service:

```
SEARXNG_URL=https://google-search-searxng.onrender.com
```

## Environment variables

- `SEARXNG_URL` — URL where SearxNG is reachable (default: `http://localhost:8080`).

## Endpoints

- `GET /` — serves the frontend `index.html`
- `GET /api/status` — health check
- `POST /search` — search API; JSON body: `{ "query": "your query" }`

## Tests

Run tests with:

pytest


