# Annual Leave Seed Corpus

Place formal Annual Leave and Leave Management source-authority documents here.

Use this folder for curated platform knowledge only:

- Developer Logs
- Hardening Logs
- Platform Doctrine or doctrine supplements
- Formal requirements or planning documents, if they are intended as source evidence

Do not place raw chat-history exports in this folder. Raw chat history is lower-authority supporting material and should not be bulk-loaded until formal logs and doctrine have been tested first.

After copying candidate TXT/DOCX files here, scan them and build a draft manifest from the repository root:

```powershell
py scripts/scan_leave_corpus_candidates.py samples/knowledge/annual_leave_seed
py scripts/build_leave_manifest_from_candidates.py samples/knowledge/annual_leave_seed --output samples/knowledge/annual_leave_seed_manifest.generated.json --min-score 3
```
