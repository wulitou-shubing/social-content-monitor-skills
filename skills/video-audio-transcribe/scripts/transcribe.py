#!/usr/bin/env python3
"""Transcribe a local media file into timestamped text and/or SRT."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
from typing import Any


OFFICIAL_HF_ENDPOINT = "https://huggingface.co"


def srt_time(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    whole_seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"


def configure_hugging_face(endpoint: str) -> None:
    os.environ["HF_ENDPOINT"] = endpoint
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")


def load_model(args: argparse.Namespace) -> Any:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("faster-whisper is not installed. Install requirements.txt after user approval.") from exc

    kwargs: dict[str, Any] = {"device": args.device, "compute_type": args.compute_type}
    if args.cache_dir:
        kwargs["download_root"] = str(Path(args.cache_dir).expanduser())

    configure_hugging_face(args.hf_endpoint)
    try:
        return WhisperModel(args.model, **kwargs)
    except Exception:
        if not args.fallback_to_official or args.hf_endpoint == OFFICIAL_HF_ENDPOINT:
            raise
        print("[transcribe] configured model source failed; retrying the official Hugging Face endpoint", flush=True)
        configure_hugging_face(OFFICIAL_HF_ENDPOINT)
        return WhisperModel(args.model, **kwargs)


def transcribe(args: argparse.Namespace) -> list[Path]:
    source = Path(args.media).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Media file does not exist: {source}")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    base = Path(args.output_name).stem if args.output_name else source.stem

    model = load_model(args)
    options: dict[str, Any] = {"beam_size": args.beam_size, "vad_filter": not args.no_vad}
    if args.language != "auto":
        options["language"] = args.language

    segments_iter, info = model.transcribe(str(source), **options)
    segments = list(segments_iter)
    created: list[Path] = []

    if args.format in {"txt", "both"}:
        txt_path = output_dir / f"{base}_transcript.txt"
        with txt_path.open("w", encoding="utf-8") as handle:
            handle.write(f"source: {source.name}\n")
            handle.write(f"duration_seconds: {info.duration:.1f}\n")
            handle.write(f"language: {info.language}\n")
            handle.write(f"language_probability: {info.language_probability:.4f}\n")
            handle.write(f"model: {args.model}\n")
            handle.write("=" * 60 + "\n")
            for segment in segments:
                handle.write(f"[{segment.start:07.1f} - {segment.end:07.1f}] {segment.text.strip()}\n")
        created.append(txt_path)

    if args.format in {"srt", "both"}:
        srt_path = output_dir / f"{base}.srt"
        with srt_path.open("w", encoding="utf-8") as handle:
            for index, segment in enumerate(segments, start=1):
                handle.write(f"{index}\n")
                handle.write(f"{srt_time(segment.start)} --> {srt_time(segment.end)}\n")
                handle.write(f"{segment.text.strip()}\n\n")
        created.append(srt_path)

    print(
        f"[transcribe] language={info.language} probability={info.language_probability:.2f} "
        f"duration={info.duration:.1f}s model={args.model}",
        flush=True,
    )
    for path in created:
        print(path)
    return created


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--output-name")
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="auto")
    parser.add_argument("--format", choices=("txt", "srt", "both"), default="both")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--no-vad", action="store_true")
    parser.add_argument("--cache-dir")
    parser.add_argument("--hf-endpoint", default=os.environ.get("HF_ENDPOINT", OFFICIAL_HF_ENDPOINT))
    parser.add_argument("--fallback-to-official", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        transcribe(args)
        return 0
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: model loading or transcription failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
