#!/usr/bin/env python3
"""Extract an MP3 audio track from a local media file with ffmpeg."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys


def ffmpeg_command() -> str:
    configured = os.environ.get("FFMPEG_CMD", "ffmpeg")
    resolved = shutil.which(configured)
    if not resolved:
        raise RuntimeError("ffmpeg is not installed or FFMPEG_CMD is invalid.")
    return resolved


def extract(args: argparse.Namespace) -> Path:
    source = Path(args.media).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Media file does not exist: {source}")
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    name = Path(args.output_name).stem if args.output_name else source.stem
    destination = output_dir / f"{name}.mp3"

    command = [
        ffmpeg_command(),
        "-y",
        "-i",
        str(source),
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        args.bitrate,
        "-ar",
        str(args.sample_rate),
        str(destination),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0 or not destination.is_file() or destination.stat().st_size == 0:
        raise RuntimeError(f"Audio extraction failed.\n{result.stderr[-1200:]}")
    print(destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--output-name")
    parser.add_argument("--bitrate", default="192k")
    parser.add_argument("--sample-rate", type=int, default=44100)
    args = parser.parse_args()
    try:
        extract(args)
        return 0
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
