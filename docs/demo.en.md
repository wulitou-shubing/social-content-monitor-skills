# Sanitized demo

This fictional example shows the result produced when the two Skills work together. It contains no real creator, Lark URL, account ID, cookie, or downloaded media.

## User request

```text
Monitor my configured public creator accounts. Process only posts published after the baseline, save their metadata to Lark Base, and generate timestamped transcripts for videos with speech.
```

## Discovered post

| Field | Example value |
| --- | --- |
| Platform | douyin |
| Content ID | demo-20260812-001 |
| Unique key | douyin:demo-20260812-001 |
| Content type | video |
| Author | Example Creator |
| Title | Organize one industry update in three steps |
| Published | 2026-08-12 09:30 |
| Transcription status | completed |

## Timestamped source transcript

```text
[00:00.00] Today I will use three steps to organize an industry update.
[00:03.20] First, identify the source. Second, verify the date and original text.
[00:07.80] Finally, record the conclusion separately from anything that remains uncertain.
```

## Write sequence

1. The monitoring Skill verifies authorship and the stable content ID.
2. It queries Lark with the unique key and confirms that the post is new.
3. It creates the metadata record with transcription status `pending`.
4. The transcription Skill downloads authorized media and produces the timestamped transcript.
5. The monitoring Skill updates the original Lark record with the transcript and final status.

If download or recognition fails, the metadata remains available and the status becomes `failed`. A later retry updates the same record instead of creating a duplicate row.
