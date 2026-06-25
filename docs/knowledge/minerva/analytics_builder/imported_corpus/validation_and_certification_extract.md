# Validation And Certification Extract

Source files:

- `metadata/analytics_builder/validation_manifest.v0_1.json`
- `metadata/analytics_builder/certification_evidence_packets.v0_1.json`
- `metadata/analytics_builder/certification_readiness_report.v0_1.json`
- `metadata/analytics_builder/certification_rules.v0_1.json`
- `metadata/analytics_builder/prohibited_claims.v0_1.json`

## Validation And Evidence Counts

- Validation assets: 6.
- Validation gaps: 4.
- Certification evidence packets: 22.
- Certified assets: 0.

## Certification Readiness Posture

Current Certified asset count remains zero. Diagnostic and Transitional assets may be useful with warnings, but they are not Certified. Blocked assets require upstream proof before promotion.

The certification readiness report records 9 dataset readiness entries and 13 recipe readiness entries. It also records validation gaps and blocked-gap summaries.

## Minerva Use

Minerva may use this extract to evaluate answers about validations, evidence packets, certification readiness, and why no assets are Certified.

## Safety Notes

- Validation passing is evidence, not automatic certification.
- Visual rendering is not certification proof.
- Export is not publishing unless a governed publishing workflow says so.
- Refresh/update is not certification.
- Minerva must not mark any asset Certified unless governed source metadata says Certified.
