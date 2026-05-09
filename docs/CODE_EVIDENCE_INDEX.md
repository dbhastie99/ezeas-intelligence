# Code Evidence Index

The Code Evidence Index is Minerva's foundation for discovering code evidence in a repository without exposing code content. It produces metadata that can be reviewed, approved, and converted into a future ingestion plan.

## Current Supported State

The current implementation is metadata-only. It can:

- scan a local repository for supported code, configuration, schema, migration, API contract, manifest, and documentation files;
- classify included files by `source_type`, `language`, and `file_kind`;
- resolve Git repository metadata with read-only Git commands;
- export a scanner manifest with `safety_summary`, `repository_metadata`, approval metadata, and validation results;
- create and review an approval manifest;
- manually update approval review fields for selected files;
- build and review a metadata-only ingestion plan from approved files.

## Scanner

`scripts/scan_code_evidence.py` performs a dry-run metadata scan. It records file paths, classification metadata, Git metadata where available, exclusion reasons, safety metadata, and validation results.

The scanner does not read or store file contents. It may inspect small byte samples only to detect binary files and exclude them; those bytes are not exported.

## Approval Manifest

The approval manifest is a human-reviewable JSON artifact. It starts with:

- `approval_required: true`
- `approval_status: PENDING_REVIEW`
- `approved_file_count: 0`
- `rejected_file_count: 0`

Each included file starts with:

- `review_status: PENDING_REVIEW`
- `review_notes: []`
- `proposed_ingestion_action: DO_NOT_INGEST_YET`

Approval editing currently changes only review metadata in the approval manifest. It does not approve ingestion into any database or retrieval system.

## Metadata-Only Ingestion Plan

`scripts/build_code_metadata_ingestion_plan.py` creates a planning artifact from an approval manifest. It includes only files marked:

- `review_status: APPROVED`
- `proposed_ingestion_action: INGEST_METADATA_ONLY`

The plan contains metadata only. It is not an ingestion implementation and does not write to any database.

## Explicitly Not Implemented

The following are intentionally not implemented in the current foundation:

- database ingestion of code evidence;
- code content extraction or storage;
- code content chunking;
- symbol extraction;
- embeddings or vector indexing for code evidence;
- chat, retrieval, or answer-generation access to code evidence;
- execution of scanned repository code;
- mutation of scanned repository source files.

## Safety Guarantees

Current Code Evidence Index tooling guarantees:

- no code content captured;
- no database ingestion;
- no LLM exposure;
- no code execution;
- no source repository mutation.

Scanner and plan safety fields must remain false or zero:

- `code_content_captured: false`
- `included_code_content_bytes: 0`
- `database_ingestion_performed: false`
- `llm_exposure_performed: false`
- `code_content_included: false`
- `code_content_bytes: 0`
- `db_ingestion_performed: false`
- `execution_performed: false`

## CLI Workflow

1. Scan a repository:

```powershell
python scripts/scan_code_evidence.py --repo-path <repo> --repo-name <name> --output scanner.json --approval-manifest approval.json
```

2. Review approval status:

```powershell
python scripts/review_code_approval_manifest.py --manifest approval.json
```

3. Update review metadata for one file:

```powershell
python scripts/update_code_approval_manifest.py --manifest approval.json --file-path src/main.py --review-status APPROVED --proposed-ingestion-action INGEST_METADATA_ONLY --note "Reviewed for metadata-only planning."
```

4. Build a metadata-only ingestion plan:

```powershell
python scripts/build_code_metadata_ingestion_plan.py --approval-manifest approval.json --output code-metadata-plan.json
```

5. Review the plan:

```powershell
python scripts/review_code_metadata_ingestion_plan.py --plan code-metadata-plan.json
```

## Future Stages

Future work should remain gated and explicit:

- approved metadata DB ingestion design;
- code symbol extraction design;
- code content chunking only after explicit approval and secret controls;
- answer-generation integration only after audience and permission guardrails exist.
