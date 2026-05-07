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

## Slice 1.2 — Local SQL Server Run Proof

This proof shows that Minerva can run locally against SQL Server database `ezeas-intelligence-db`. It does not use the operational payroll database. It does not ingest JSON, call an external LLM, use embeddings, or execute autonomous actions.

### A. Create The Database In SSMS

1. Open SQL Server Management Studio.
2. Connect to your local SQL Server instance.
3. Open and run:

```text
scripts/create_db.sql
```

4. Switch to database `ezeas-intelligence-db`.
5. Open and run:

```text
scripts/create_tables.sql
```

The scripts create the Minerva database and the five Slice 1.x tables if they do not already exist.

### B. Configure Environment

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Set `MINERVA_DATABASE_URL` for local SQL Server. Example for Windows Integrated auth with ODBC Driver 18:

```text
MINERVA_DATABASE_URL=mssql+pyodbc:///?odbc_connect=Driver%3D%7BODBC+Driver+18+for+SQL+Server%7D%3BServer%3Dlocalhost%3BDatabase%3Dezeas-intelligence-db%3BTrusted_Connection%3Dyes%3BEncrypt%3Dyes%3BTrustServerCertificate%3Dyes%3B
MINERVA_ENV=local
MINERVA_LLM_PROVIDER=stub
MINERVA_CHUNK_SIZE=1200
MINERVA_CHUNK_OVERLAP=150
```

`TrustServerCertificate=yes` is for local development. Keep the actual operational payroll database separate and do not point Minerva at it.

### C. Install And Run The Proof

From PowerShell or the PyCharm terminal:

```powershell
pip install -r requirements.txt
python scripts/check_sqlserver_tables.py
python scripts/local_smoke_test.py
uvicorn app.main:app --reload
```

If your Windows machine uses the Python launcher, use `py` instead of `python`:

```powershell
py -m pip install -r requirements.txt
py scripts/check_sqlserver_tables.py
py scripts/local_smoke_test.py
py -m uvicorn app.main:app --reload
```

### D. Expected Smoke Result

`scripts/check_sqlserver_tables.py` should report that all expected tables exist and print row counts for:

- `KnowledgeDocument`
- `KnowledgeChunk`
- `KnowledgeChatSession`
- `KnowledgeChatMessage`
- `AIInteractionAudit`

`scripts/local_smoke_test.py` should print:

- health result with `status=ok`;
- sample document ingestion result;
- `duplicate=true` on repeat runs for the same sample document;
- a chat answer from the stub LLM;
- source reference count greater than zero;
- an audit id.

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

Tests use SQLite in memory so normal pytest runs do not require SQL Server.

```powershell
pytest
```

## Guardrails

- No external LLM calls are made in v0.1.
- No JSON evidence ingestion is implemented.
- Retrieved document content is treated as evidence, not instructions.
- Minerva does not execute actions based on retrieved text.
- Tenant fields and tenant-aware retrieval structure are present for later RBAC hardening.
