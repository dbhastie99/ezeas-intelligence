# Owner-review boundary

This slice stops at implementation, verification, canonical convergence and owner-review readiness.

It does not claim owner acceptance or certification, does not create or update a certified Leave Context Pack, and does not alter v1.9. The context disposition remains `CONTEXT_DELTA_PENDING_OWNER_ACCEPTANCE`.

Owner review should test the exact questions listed below across the available persona selector and inspect diagnostics for `LIVE_LLM_USED` versus governed fallback:

1. Does my entitlement start from employment regardless of age?
2. Does service start from my first day?
3. Am I entitled after seven years?
4. Does age affect long service leave?
5. If I started at 17, when does my entitlement begin?
6. When do I qualify for long service leave?
7. I have worked here for ten years. Am I entitled now?

Expected boundary: absence is described only as absence from governed policy rules; recognised service is kept distinct from access/vesting/payment; and no individual outcome is determined because `WorkerSpecificContextIncluded=false`.

Fallback is an acceptable governed result when diagnostics record one of the strengthened validation codes. It must not be presented as live success.

Owner-review runtime:

- location: `C:\Projects\ezeas-intelligence-leave-runtime-20260814`
- listen address: `http://127.0.0.1:8001`
- start command from that directory: `C:\Projects\.venv-workspace\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001`
- `GET /health`: `ok`
- OpenAPI route: `/api/v1/minerva/leave-studio/conversations`
- product authority verified during refresh: `65831b0983e83096db889ea4447169d88843ad63`

The final owner-path smoke attempted the live provider and correctly used governed fallback with `validation_negative_inference_claim`; it carried an audit identity and `NoChangesMade=true`. This is readiness evidence, not owner acceptance.
