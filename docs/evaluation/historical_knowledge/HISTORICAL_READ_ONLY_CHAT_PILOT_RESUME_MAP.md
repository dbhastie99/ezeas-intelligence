# Historical Read-Only Chat Pilot Resume Map

Version: v0.1

Date: 16 May 2026

## Purpose

This map records the next controlled slice for each future Minerva historical read-only chat pilot trigger after controlled-readiness completion and exposure deferral.

## Resume Map

| Future trigger | Next slice |
| --- | --- |
| Explicit internal exposure approval supplied | internal exposure candidate |
| Live LLM requested | LLM policy/safety gate |
| Final natural-language answer requested | final-answer generation gate |
| Public/tenant/customer exposure requested | production exposure gate |
| No approval supplied | remain deferred |

## Non-Authorisation

No trigger itself authorises exposure, LLM calls, final answers, DB access, corpus mutation, or production use.

Each trigger only identifies the next control slice to prepare. The next slice must still carry explicit approval, satisfy its entry criteria, and preserve all boundaries not expressly approved.
