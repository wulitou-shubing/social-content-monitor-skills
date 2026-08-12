# Recurring automation

Create or update a recurring automation only when the user explicitly requests it.

## Scheduling rules

1. Store the user's IANA timezone, for example `Asia/Shanghai`.
2. Use the product automation tool rather than hand-written cron or raw scheduler directives.
3. Put the timezone and intended local times into the automation request.
4. Add a runtime hard gate: compute current time in the configured timezone and exit before browsing when it is outside an approved window.
5. Keep one automation for one monitoring configuration so checkpoints and deduplication remain consistent.
6. Do not create duplicate schedules for the same config.

Allow a small execution window around each scheduled local time to accommodate scheduler latency. The window must not be wide enough to overlap another run.

## Run ordering

- Reject or skip overlapping runs.
- Process platforms, accounts, candidates, downloads, transcriptions, and Lark writes serially unless the user explicitly approves a tested concurrency strategy.
- A new scheduled wakeup must not start while the prior cycle is still active.

## Notifications

Default recommended behavior:

- new content: notify with per-item outcome;
- no changes: no notification;
- verification, authentication, schema, download, transcription, or write failure: notify;
- skipped outside the runtime time gate: no notification unless repeated.
