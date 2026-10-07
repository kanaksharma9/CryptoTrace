$ErrorActionPreference = "Stop"
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host "created .env" }
Push-Location backend
if (-not (Test-Path .venv)) { py -3.11 -m venv .venv }
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
Pop-Location
if (Test-Path frontend\package.json) { Push-Location frontend; npm ci; Pop-Location }
Write-Host "Bootstrap done. Next: .\scripts\dev-up.ps1"
