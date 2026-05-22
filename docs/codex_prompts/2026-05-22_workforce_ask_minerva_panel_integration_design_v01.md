# Prompt Artefact: Workforce Ask Minerva Panel Integration Design v0.1

Date: 2026-05-22

Objective: implement the Minerva design/control slice for Workforce Ask Minerva Panel Integration v0.1.

Scope:

- create design/control artefacts before wiring an Ask Minerva panel into Workforce Platform;
- recommend the first Workforce surface;
- define request payload, role mapping, source scopes, fixture/demo mode, response consumption, role-safe evidence handling, runtime evidence gap, safety boundaries, and deferred items;
- add focused tests for the design artefacts.

Required output artefacts:

- `docs/diagnostics/workforce_ask_minerva_panel_integration_design_v0_1.md`;
- `docs/diagnostics/workforce_ask_minerva_panel_integration_design_v0_1.json`;
- `docs/knowledge/workforce_ask_minerva_panel_integration_v0_1.md`;
- `docs/evaluation/workforce_ask_minerva_panel_integration_v0_1/ANSWER_EVALUATION_BASELINE.md`;
- `docs/codex_prompts/2026-05-22_workforce_ask_minerva_panel_integration_design_v01.md`;
- `tests/test_workforce_ask_minerva_panel_integration_design.py`.

Strict non-goals:

- no Workforce Platform code changes;
- no UI implementation;
- no live LLM calls;
- no DB connection;
- no database migrations;
- no chat persistence;
- no live runtime evidence fetch;
- no operational payroll evidence ingestion;
- no vector search or embeddings;
- no external API calls;
- no code execution;
- no mutation of external repos;
- no payroll calculation;
- no write actions;
- no customer production exposure.

Verification commands:

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_workforce_ask_minerva_panel_integration_design.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_panel_response_service.py tests/test_internal_chat_endpoint_smoke_harness.py tests/test_internal_chat_api_stub_fixture_key.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```
