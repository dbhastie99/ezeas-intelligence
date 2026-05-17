# Evidence Source-Status Boundary v0.1

## Purpose

Preserve the distinction between evidence existence and implementation, runtime, deployment, or production truth.

## Source Status Values

- `CONTROLLED_READINESS_EVIDENCE`
- `PLANNING_EVIDENCE`
- `ANALYSIS_EVIDENCE`
- `IMPLEMENTATION_CANDIDATE_EVIDENCE`
- `RUNTIME_EVIDENCE`
- `DEPLOYMENT_EVIDENCE`
- `PRODUCTION_EVIDENCE`
- `UNKNOWN_REQUIRES_REVIEW`

## Evidence Exists vs Implementation Truth

Evidence may exist without proving implementation truth. The boundary service records evidence status and prohibited inferences separately.

## Planning vs Implementation

Planning evidence does not imply implementation. Implementation claims require explicit proof in a future authorised phase.

## Analysis vs Repair

Analysis evidence does not imply that repair, remediation, or fix completion has occurred.

## Controlled Readiness vs Runtime

Controlled-readiness evidence does not imply runtime enablement, runtime readiness, deployment readiness, or production readiness.

## Runtime vs Deployment vs Production

Runtime, deployment, and production evidence statuses are distinct. Each requires explicit proof before its corresponding claim can be permitted.

## Required Caveats

Each status returns caveats that state what the evidence does not prove. Unknown evidence requires review.

## Prohibited Inferences

The model prohibits unsupported inferences such as implementation completed, repair completed, runtime enabled, deployed, deployment ready, production ready, or production claim without explicit proof.

## Developer Handoff

Call `build_evidence_source_status_boundary(metadata)` to evaluate source-status metadata. Use its caveats and prohibited inferences in future intake planning records.
