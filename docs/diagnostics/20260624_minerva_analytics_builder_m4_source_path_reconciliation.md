# Minerva Analytics Builder M4 Source Path Reconciliation Diagnostic

Status: source paths reconciled; governed import still required before M5 answer baselines.

Findings:

* `C:\Projects\ezeas-analytics` exists.
* Git tag `analytics-builder-static-omg-v0.2-20260624` exists.
* M1 expected `docs/analytics_builder/...` paths are stale or wrong.
* Actual canonical metadata paths are under `metadata/analytics_builder/`.
* Actual guide markdown paths are under `docs/analytics_builder_guide/`.
* Actual generated guide HTML is under `docs/generated/analytics_builder_guide/`.
* Generated HTML should be reference-only and not bulk copied.
* M5 answer baselines remain blocked pending governed import manifest and count reconciliation.

No source repo modifications were made. No runtime behavior was implemented. No final-paid, certification, or trust posture changed.

