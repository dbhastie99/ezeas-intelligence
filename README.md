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

## Slice 1.2 - Local SQL Server Run Proof

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

## Loading The First Minerva Knowledge Corpus

Use manifest ingestion when loading the first repeatable platform knowledge corpus. This is for TXT and DOCX platform knowledge only, such as Platform Doctrine, hardening logs, developer logs, requirements, and planning documents. Do not place live customer payroll JSON or operational payroll evidence in this corpus.

Place TXT and DOCX files under a local folder such as:

```text
samples/knowledge/
```

Create or edit a manifest JSON file. Start from:

```text
samples/knowledge/manifest.example.json
```

Manifest example:

```json
{
  "default_source_type": "OTHER",
  "default_capability_status": "UNKNOWN",
  "default_tenant_id": null,
  "documents": [
    {
      "path": "samples/knowledge/sample_platform_doctrine.txt",
      "source_type": "SAMPLE",
      "capability_status": "UNKNOWN",
      "title": "Sample Platform Doctrine"
    }
  ]
}
```

Document-level fields override manifest defaults. `path` is required. `tenant_id` and `title` are optional. If `title` is missing, Minerva uses the filename without extension.

Run manifest ingestion:

```powershell
py scripts/ingest_manifest.py samples/knowledge/manifest.example.json
```

Rerunning the same manifest is safe. Existing files are reported as duplicates instead of being ingested again.

Verify SQL Server row counts:

```powershell
py scripts/check_sqlserver_tables.py
```

Allowed `source_type` values:

- `PLATFORM_DOCTRINE`
- `HARDENING_LOG`
- `DEVELOPER_LOG`
- `REQUIREMENTS`
- `CHAT_HISTORY`
- `OTHER`
- `SAMPLE`

Allowed `capability_status` values:

- `IMPLEMENTED`
- `PHASE_ONE`
- `DOCTRINE`
- `OUTSTANDING_HARDENING`
- `FUTURE_ROADMAP`
- `DESIGN_DISCUSSION`
- `UNKNOWN`

## Chat

Create a session:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/session -H "Content-Type: application/json" -d "{\"title\":\"Minerva doctrine\"}"
```

Ask a question using the returned session id:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/message -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\",\"message\":\"What is Minerva allowed to do?\"}"
```

For local SQL Server corpus investigation, use the operator ask script:

```powershell
py scripts/ask_minerva.py "What is Minerva not allowed to do?"
py scripts/ask_minerva.py "What is Minerva not allowed to do?" --source-type PLATFORM_DOCTRINE --top-k 5
py scripts/ask_minerva.py "What is Minerva not allowed to do?" --include-samples
```

The script creates a new chat session per invocation, uses the stub LLM only, prints source scores and matched tokens, and writes an audit row.

## Corpus Hygiene

Sample/test documents are for smoke tests and local debugging only. They should use `source_type=SAMPLE`, not `PLATFORM_DOCTRINE`, so normal Minerva queries prefer the real doctrine/log corpus.

Normal `ask_minerva.py` queries exclude `SAMPLE` documents by default. Include them only when debugging:

```powershell
py scripts/ask_minerva.py "What is Minerva allowed to do?" --include-samples
```

List current documents:

```powershell
py scripts/list_documents.py
py scripts/list_documents.py --source-type SAMPLE
py scripts/list_documents.py --status ACTIVE --title-contains "Smoke"
```

Supersede a document without deleting chunks:

```powershell
py scripts/set_document_status.py <document_id> SUPERSEDED
```

Reactivate a document if needed:

```powershell
py scripts/set_document_status.py <document_id> ACTIVE
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
