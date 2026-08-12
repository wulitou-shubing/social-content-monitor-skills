# Security Policy

## Supported version

Security fixes are applied to the latest version on the `main` branch.

## Reporting a vulnerability

Please do not open a public Issue for a vulnerability that could expose credentials, browser sessions, private account data, or Lark records.

Use the repository's private vulnerability reporting feature when it is available. If that feature is unavailable, open a short Issue without sensitive details and ask the maintainer for a private contact channel.

Include the affected Skill, the smallest safe reproduction, the expected impact, and any suggested mitigation. Remove tokens, cookies, private URLs, local paths, personal information, and downloaded media before sending a report.

## Security boundaries

The Skills in this repository must not

- bypass CAPTCHA, login verification, rate limits, private accounts, or paywalls
- export or print browser cookies and access tokens
- follow instructions embedded in untrusted pages, captions, subtitles, or comments
- publish, message, follow, like, or comment on a user's behalf
- commit working configuration, monitoring state, downloaded media, or transcripts containing private data

Authenticated access must use the user's normal authorized session. Actions that install software, use browser credentials, change Lark schemas, or create schedules require the user's approval.
