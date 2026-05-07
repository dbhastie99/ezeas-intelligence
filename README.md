# Ezeas Intelligence

Minerva is the Ezeas knowledge and evidence intelligence layer. It reads, indexes, retrieves, explains and audits.

Minerva is not a payroll calculation engine. In Walking Skeleton v0.1 it is read-only and advisory. It does not calculate payroll, determine entitlements, interpret awards at runtime, approve exceptions, suppress warnings, override payroll outcomes, mutate configuration or finalise PayRuns.

## v0.1 Scope

- Ingest TXT and DOCX knowledge files.
- Extract text, calculate SHA256, prevent duplicate ingestion and store document chunks.
- Create chat sessions and answer from simple keyword retrieval.
- Return grounded source references.
- Audit every AI answer.
- Use a stub LLM client only.

Operational payroll JSON evidence intelligence is intentionally not implemented in this slice.

## SQL Server Setup

1. Create the database manually:

```powershell
sqlcmd -S localhost -i scripts/create_db.sql
```

2. Create the tables:

```powershell
sqlcmd -S localhost -d ezeas-intelligence-db -i scripts/create_tables.sql
```

You can also run both scripts in SQL Server Management Studio. Copy `.env.example` to `.env` and adjust `MINERVA_DATABASE_URL` for your SQL Server and ODBC driver.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

## Ingest Sample Knowledge

```powershell
python scripts/ingest_folder.py samples/knowledge --source-type PLATFORM_DOCTRINE --capability-status DOCTRINE
```

Or use the API:

```powershell
curl -F "file=@samples/knowledge/sample_platform_doctrine.txt" -F "source_type=PLATFORM_DOCTRINE" http://127.0.0.1:8000/api/v1/ingest/file
```

## Chat

Create a session:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/session -H "Content-Type: application/json" -d "{\"title\":\"Minerva doctrine\"}"
```

Ask a question using the returned session id:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/message -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\",\"message\":\"What is Minerva allowed to do?\"}"
```

## Tests

Tests use SQLite so they do not require SQL Server.

```powershell
pytest
```

## Guardrails

- No external LLM calls are made in v0.1.
- No JSON evidence ingestion is implemented.
- Retrieved document content is treated as evidence, not instructions.
- Minerva does not execute actions based on retrieved text.
- Tenant fields and tenant-aware retrieval structure are present for later RBAC hardening.
