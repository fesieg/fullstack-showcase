# Bottle Return System Backend

A simple FastAPI backend for managing bottle returns, with SQLite storage, CORS, logging. Easily run locally or with Docker.

## Quickstart

### 1. Requirements
- Python 3.10+
- (Optional) Docker & Docker Compose

### 2. Init (local)

Assumption is that you have uv installed

```bash
cd backend
uv venv
source venv/bin/activate

# to install everything (including dev deps):
uv sync
pre-commit install
# or to just install necessary deps for the app to run:
uv pip install -e .

```

### 3. Run the App (Local)
```bash
cd backend
./scripts/start-dev.sh # or just start.sh for no hot reload
```

- The API will be available at http://localhost:8000/api
- Interactive docs: http://localhost:8000/docs

### 4. Run Tests
```bash
cd backend
pytest
```

---

## Docker Deployment

### 1. Build & Run with Docker Compose
```bash
# Build and start the backend
# (First time may take a minute)
docker-compose up --build
```
- The API will be available at http://localhost:8000/api

### 2. Stop the App
```bash
docker-compose down
```

---

## File Structure
- `app/` - FastAPI app code (endpoints, models, services, etc)
- `tests/` - Pytest test suite
- `scripts/` - Start scripts for Docker
- `bottles_refund_system.db` - SQLite database (auto-created)

---

## Configuration (.env)

You can configure the backend using a `.env` file in the backend project root (next to `pyproject.toml`).

**Example `.env`:**
```
DB_URL=./bottles_refund_system.db
SEED_DB=false
API_TOKEN=your-secret-token
```
- `DB_URL`: Path to the SQLite database file (default: `./bottles_refund_system.db`)
- `SEED_DB`: Set to `true` to seed the database on startup if empty (default: `false`)
- `API_TOKEN`: Static API token for testing authentication (required)

The backend will automatically load these settings on startup.

---

## Notes
- The backend is stateless except for the SQLite DB file.
- For development, DB is stored as `bottles_refund_system.db` in `backend/`.
- For production, we would mount a volume or use a managed DB.
- CORS is enabled for local frontend development.