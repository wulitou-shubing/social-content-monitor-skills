---
name: video-audio-transcribe
description: Download supported online media or process local video/audio files, optionally extract MP3 audio, and transcribe speech into timestamped text or SRT with faster-whisper. Use when users ask to download a video, extract audio, convert speech to text, create a transcript/subtitle file, or when another skill needs a reusable media transcription step. Supports yt-dlp-compatible sites, including Douyin when the user has a permitted authenticated browser session.
---

# Video Audio Transcribe

Use this skill as a media-processing building block. Keep downloading, audio extraction, transcription, and editorial cleanup as separate stages so failures remain recoverable.

## Select the shortest workflow

1. For an online URL, run `scripts/download_video.py`.
2. For a local video when the user requests MP3, run `scripts/extract_audio.py`.
3. For transcription, pass either the local video or audio file directly to `scripts/transcribe.py`.
4. Preserve the timestamped result as the evidence copy. Create a separately named cleaned version if editorial cleanup is requested.

Do not extract MP3 merely to feed Whisper; faster-whisper can read common video containers directly.

## Prepare the runtime

Before the first run, read [references/runtime.md](references/runtime.md). Do not silently install dependencies. Ask before installing packages or system software.

## Download online media

```bash
python scripts/download_video.py "<URL>" --output-dir "<DIR>"
```

Use `--cookies-from-browser chrome` only when the target site requires the user's authenticated session and the user has approved access. Never enable browser cookies for every site by default. A cookie or session file must never be committed, copied into the skill, or printed.

For a custom filename:

```bash
python scripts/download_video.py "<URL>" --output-dir "<DIR>" --filename "<NAME>"
```

Stop instead of retrying when a site displays CAPTCHA, login verification, rate limiting, or an explicit access denial. Do not bypass platform controls. Read [references/privacy-and-rights.md](references/privacy-and-rights.md) before authenticated downloading.

## Extract MP3 when requested

```bash
python scripts/extract_audio.py "<VIDEO>" --output-dir "<DIR>" --bitrate 192k
```

This requires `ffmpeg`. Preserve the original video unless the user explicitly asks to remove it.

## Transcribe speech

```bash
python scripts/transcribe.py "<MEDIA>" --output-dir "<DIR>" --model small --language auto --format both
```

- Use `small` for routine work.
- Use `medium` or `large-v3` only when accuracy justifies extra download and compute time.
- Use `--language zh` or another language code when known.
- The default model source is the official Hugging Face endpoint. For a user-approved mirror, pass `--hf-endpoint`; use `--fallback-to-official` only when network policy permits official fallback.
- Run long transcriptions in a persistent/background session and report progress.

## Clean the transcript

Treat Whisper output as a draft. You may add punctuation, merge broken lines, and fix only obvious errors supported by context. Do not silently invent missing speech or guess uncertain names, figures, brands, tickers, medical terms, or legal terms. Flag uncertain passages and retain the timestamped source for review.

## Deliver results

Report:

- source file and generated files;
- detected language and media duration;
- model used;
- any download, audio, or recognition limitations;
- terms or figures that require manual verification.
