docker compose up -d postgres neo4j redis minio minio-init
docker compose ps
Write-Host "Run migrations: cd backend ; .\.venv\Scripts\Activate.ps1 ; alembic upgrade head"
