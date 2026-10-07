# CryptoTrace Developer & Deployment Runbook

This document details environment setup, local development workflow, Docker operations, and troubleshooting procedures for CryptoTrace.

---

## 1. Quick Start (Windows PowerShell)

Run the bootstrap script from the repository root:
```powershell
.\scripts\bootstrap.ps1
```

This will:
- Copy `.env.example` to `.env` if `.env` does not exist.
- Initialize Python 3.11 virtual environment in `backend\.venv`.
- Install backend dependencies from `requirements.txt` and `requirements-dev.txt`.
- Install frontend dependencies (`npm ci` / `npm install`).

Start local infrastructure containers:
```powershell
.\scripts\dev-up.ps1
```

To stop containers:
```powershell
.\scripts\dev-down.ps1
```

---

## 2. Docker Service Profiles & Ports

| Service | Profile | Port | URL / Purpose |
| :--- | :--- | :--- | :--- |
| **web** | `app` | `3000` | http://localhost:3000 (Next.js Dashboard) |
| **api** | `app` | `8000` | http://localhost:8000/docs (FastAPI Swagger & SSE) |
| **sahyog-mock** | `app` | `8100` | http://localhost:8100 (Mock SAHYOG / NCRP portal) |
| **postgres** | `default` | `5432` | PostgreSQL database |
| **neo4j** | `default` | `7474`, `7687` | http://localhost:7474 (Neo4j Browser, bolt://7687) |
| **redis** | `default` | `6379` | Redis pub/sub & Celery broker |
| **minio** | `default` | `9000`, `9001` | http://localhost:9001 (MinIO Console, user: `ctminio`) |
| **mlflow** | `ml` | `5000` | http://localhost:5000 (MLflow Tracking Server) |
| **prometheus** | `monitoring` | `9090` | http://localhost:9090 |
| **grafana** | `monitoring` | `3001` | http://localhost:3001 (Admin / Admin) |
| **caddy** | `edge` | `8443` | https://localhost:8443 (TLS 1.3 Reverse Proxy) |

---

## 3. Useful Operational Commands

### Database Migrations (Alembic)
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

### Export OpenAPI Contracts Schema
```powershell
python scripts/export_schema.py
```

### Running Backend Unit & Golden Tests
```powershell
cd backend
pytest -q -m "not integration"
```

---

## 4. Troubleshooting Guide

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `docker: error during connect` | Docker Desktop is not running or WSL2 is stopped | Launch Docker Desktop; run `wsl --update` |
| `Neo4j container restarts / OOM` | High memory usage in WSL2 | Lower Neo4j heap memory in `docker-compose.yml` or allocate 4GB+ in `.wslconfig` |
| Port conflict on `5432` / `6379` / `3000` | Local services already using standard ports | Stop local PostgreSQL/Redis services or run `netstat -ano | findstr :5432` and `taskkill /PID <pid> /F` |
| `exec ... no such file or directory` | CRLF line endings inside shell script containers | Convert line endings to LF (`git add --renormalize .`) |
| API cannot connect to DB in dev | Incorrect `DATABASE_URL` | Use `localhost` hostnames when running FastAPI directly on host, and service names inside Docker |
