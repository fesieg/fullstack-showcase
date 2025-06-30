# Bottle Deposit System – 5-Hour Showcase Project

**Features:**
- FastAPI backend with SQLite, CORS, logging, and rate limiting
- React + TypeScript frontend with SCSS and BEM methodology
- (limited) API key authentication and barcode uniqueness validation
- Docker & Docker Compose support for easy deployment
- Pytest and frontend smoke tests included
- Clean project structure and documentation
- Conventional commits

This is a full-stack showcase project for a bottle return/refund system, built with FastAPI (Python) for the backend and React (TypeScript) for the frontend. No ORM, no component framework.

---

## Quick Start

### 1. Backend
- See `backend/README.md` for full details.
- Quickstart:
  ```bash
  cd backend
  # (Recommended) Create and activate a virtualenv
  uv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  uv sync  # or: uv pip install -e .
  ./scripts/start-dev.sh  # or: uvicorn app.main:app --reload
  ```

  or

  ```
  cd backend
  docker compose up
  ```
- The API will be available at http://localhost:8000
- API docs: http://localhost:8000/docs

### 2. Frontend
- See `frontend/README.md` for full details.
- Quickstart:
  ```bash
  cd frontend
  bun install  # or: npm install (if you prefer)
  bun dev      # or: npm run dev
  ```
- The app will be available at http://localhost:5173

---

## About
This project was built within 5 hours, as a coding exercise and demonstration of (at least some) best practices for a full-stack application.

### Next steps:
What I would (and maybe will) implement next on this project:

1. Proper user authentication system and api token creation / handling.
2. Rate limiting via nginx (in the docker container). I didnt want to go over the time limit.
3. WebSocket updates instead of manually triggering reloads. I strongly prefer this over polling or manually triggering reloads, but again, time limit.
4. Possibly pagination on the backend bottles GET endpoint. Not a priority however, in view of the use case.
