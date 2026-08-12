#!/usr/bin/env python3
"""Download one media URL with yt-dlp without enabling browser cookies by default."""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse


HARD_STOP_MARKERS = (
    "captcha",
    "fresh cookies",
    "login required",
    "sign in to confirm",
    "too many requests",
    "rate limit",
    "security verification",
    "安全验证",
    "访问过于频繁",
    "验证码",
)


def yt_dlp_command() -> list[str]:
    configured = os.environ.get("YTDLP_CMD")
    if configured:
        resolved = shutil.which(configured)
        if not resolved:
            raise RuntimeError(f"YTDLP_CMD does not resolve to an executable: {configured}")
        return [resolved]
    resolved = shutil.which("yt-dlp")
    if resolved:
        return [resolved]
    if importlib.util.find_spec("yt_dlp"):
        return [sys.executable, "-m", "yt_dlp"]
    raise RuntimeError("yt-dlp is not installed. Install requirements.txt after user approval.")


def validate_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("Expected a complete http(s) media URL.")
    return value


def newest_output(directory: Path, started_at: float) -> Path | None:
    candidates = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.stat().st_mtime >= started_at - 1 and not path.name.endswith(".part")
    ]
    return max(candidates, key=lambda path: path.stat().st_mtime, default=None)


def download(args: argparse.Namespace) -> Path:
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = output_dir / "%(title)s.%(ext)s"
    if args.filename:
        output_template = output_dir / f"{Path(args.filename).stem}.%(ext)s"

    command = yt_dlp_command() + [
        "--no-playlist",
        "--newline",
        "--print",
        "after_move:filepath",
        "-f",
        args.format,
        "-o",
        str(output_template),
    ]
    if args.cookies_from_browser:
        command += ["--cookies-from-browser", args.cookies_from_browser]
    if args.cookies_file:
        command += ["--cookies", str(Path(args.cookies_file).expanduser())]
    command.append(args.url)

    started_at = time.time()
    last_output = ""
    for attempt in range(1, args.retries + 1):
        print(f"[download] attempt {attempt}/{args.retries}", flush=True)
        result = subprocess.run(command, capture_output=True, text=True)
        last_output = "\n".join(part for part in (result.stdout, result.stderr) if part)

        if result.returncode == 0:
            for line in reversed(result.stdout.splitlines()):
                candidate = Path(line.strip()).expanduser()
                if candidate.is_file() and candidate.stat().st_size > 0:
                    print(candidate.resolve())
                    return candidate.resolve()
            candidate = newest_output(output_dir, started_at)
            if candidate and candidate.stat().st_size > 0:
                print(candidate.resolve())
                return candidate.resolve()

        lowered = last_output.lower()
        if any(marker in lowered for marker in HARD_STOP_MARKERS):
            raise RuntimeError("The site requires verification, authentication, or rate-limit recovery; stopped without retrying.")
        if attempt < args.retries:
            time.sleep(args.retry_delay)

    detail = last_output[-1200:].strip()
    raise RuntimeError(f"Download failed after {args.retries} attempt(s).\n{detail}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", type=validate_url)
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--format", default="best")
    parser.add_argument("--filename")
    parser.add_argument("--cookies-from-browser", help="Browser name passed to yt-dlp, only with user approval.")
    parser.add_argument("--cookies-file", help="Existing Netscape cookie file, only with user approval.")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=3.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.retries < 1:
        raise SystemExit("--retries must be at least 1")
    try:
        download(args)
        return 0
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
