# Analytics Builder Source Path Reconciliation - M4

M4 was inserted before answer baselines because M3 found that the local `ezeas-analytics` repository exists but the M1 expected source paths were not present at the exact registered paths. Creating answer baselines before source paths are reconciled would risk grounding Minerva answers in stale assumptions.

## What M3 Found

M3 registered the Analytics Builder corpus as `static_corpus_registered_metadata_only`. It did not copy source content or generated HTML. Production answer use remained blocked.

## Expected Paths Were Stale

M1 expected source paths under `docs/analytics_builder/...`, such as:

* `docs/analytics_builder/guide_spine.md`
* `docs/analytics_builder/datasets/catalogue.md`
* `docs/analytics_builder/datasets/cards/*.md`
* `docs/analytics_builder/visual_recipes/library.md`
* `docs/analytics_builder/certification/rules.md`
* `dist/analytics_builder_guide_static/index.html`

Those exact paths were not found in the local source repository.

## Actual Source Locations

The local `ezeas-analytics` repository uses:

* `metadata/analytics_builder/` for canonical JSON metadata;
* `metadata/analytics_builder/dataset_cards/` for dataset-card JSON;
* `metadata/analytics_builder/visual_recipes/` for visual-recipe JSON;
* `metadata/analytics_builder/certification_packets/` for 22 certification evidence packet JSON files;
* `docs/analytics_builder_guide/` for guide markdown and milestone reports;
* `docs/analytics_builder_guide/demo_walkthroughs/` for demo walkthrough markdown;
* `docs/generated/analytics_builder_guide/` for generated HTML presentation output.

The expected tag `analytics-builder-static-omg-v0.2-20260624` exists locally.

## Safe For Minerva

Safe to reference by path after review:

* canonical JSON under `metadata/analytics_builder/`;
* guide markdown under `docs/analytics_builder_guide/`;
* demo walkthrough markdown under `docs/analytics_builder_guide/demo_walkthroughs/`.

Safe to copy later as compact extracts after governed review:

* selected guide markdown extracts;
* selected metadata summaries;
* selected certification packet summaries;
* selected demo walkthrough summaries.

Not safe to bulk copy:

* generated HTML under `docs/generated/analytics_builder_guide/`;
* SQL artifacts;
* any generated output as source truth.

## Remaining Unresolved

The dataset and visual-recipe counts need reconciliation before M5:

* M1 says 9 datasets, but `metadata/analytics_builder/dataset_cards/` contains 6 files. Candidate/gap dataset metadata and certification packets appear to account for remaining blocked/gap datasets.
* M1 says 13 visual recipes, but `metadata/analytics_builder/visual_recipes/` contains 10 files. `blocked_visual_recipes_v0_1.json` appears to account for blocked recipes.

## Before M5

Before answer baselines, create a governed import manifest that references the canonical JSON and markdown paths, reconciles the dataset/recipe counts, excludes generated HTML from source truth, and applies the M1 answer safety contract.

