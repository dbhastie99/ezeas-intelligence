# Analytics Builder Governed Corpus Import Plan - M4

This plan defines the safe import boundary for a later Analytics Builder corpus import slice.

## Import Method Options

`reference_only`: Keep source files in `ezeas-analytics` and register paths plus source tag.

`metadata_copy`: Copy compact JSON metadata into an approved Minerva corpus area after source review.

`compact_extract`: Create short governed extracts from source markdown or JSON with source path, tag, status, and safety notes.

`do_not_copy_generated_artifact`: Reference generated output only for lineage and presentation checks.

## Recommended Approach

Use a mixed governed approach:

1. Reference canonical source paths in `metadata/analytics_builder/`.
2. Create compact extracts from guide markdown under `docs/analytics_builder_guide/`.
3. Create compact extracts or metadata copies for dataset cards, visual recipes, certification packets, prohibited claims, validation manifest, readiness report, blocked-gap artifacts, and v0.2 closeout.
4. Reference generated HTML only after it is traced to source markdown and metadata.
5. Keep production answer use blocked until tests prove the governed import manifest covers required source groups and safety controls.

## What Not To Copy

Do not bulk copy generated HTML from `docs/generated/analytics_builder_guide/`.

Do not copy SQL files into the Minerva answer corpus for this slice.

Do not copy source material in a way that creates a second analytics truth path.

## Source Lineage

Every imported extract must include:

* source repo: `ezeas-analytics`;
* expected tag: `analytics-builder-static-omg-v0.2-20260624`;
* source path;
* artifact group;
* import method;
* proof/certification status caveats;
* safety notes from the M1 answer contract.

## Avoiding Stale Generated Truth

Generated HTML is presentation output. It can help reviewers confirm the static guide renders, but it must not be used as certification proof, final-paid proof, or canonical source truth.

## Later Manifest Updates

A later slice should update or supersede M1/M3 manifests by replacing stale `docs/analytics_builder/...` paths with the reconciled canonical paths from `metadata/analytics_builder/`, `docs/analytics_builder_guide/`, and `docs/generated/analytics_builder_guide/` reference-only entries.

## M5 Acceptance Criteria

M5 answer baselines may proceed only after:

* all required artifact groups have reconciled canonical source paths;
* dataset and visual-recipe count differences are explained;
* generated HTML is excluded from source-truth import;
* prohibited claims and safety requirements are imported or referenced;
* final-paid truth remains `UNPROVEN / Blocked`;
* current Certified asset count remains zero unless source metadata changes;
* no runtime ingestion, UI, routes, dashboards, SQL write paths, or runtime behavior changes are introduced.

