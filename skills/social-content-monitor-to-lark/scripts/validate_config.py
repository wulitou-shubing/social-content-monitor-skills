#!/usr/bin/env python3
"""Validate a social-content-monitor-to-lark JSON configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
PLATFORM_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
REQUIRED_FIELDS = {
    "unique_key",
    "platform",
    "content_id",
    "content_kind",
    "title",
    "published_at",
    "canonical_url",
    "author_name",
}


def is_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate(config: object) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(config, dict):
        return ["root must be a JSON object"], warnings

    if config.get("version") != 1:
        errors.append("version must be 1")

    timezone = config.get("timezone")
    if not isinstance(timezone, str):
        errors.append("timezone must be an IANA timezone string")
    else:
        try:
            ZoneInfo(timezone)
        except ZoneInfoNotFoundError:
            errors.append(f"unknown IANA timezone: {timezone}")

    schedule = config.get("schedule")
    if not isinstance(schedule, list) or not schedule:
        errors.append("schedule must be a non-empty list")
    elif any(not isinstance(value, str) or not TIME_PATTERN.fullmatch(value) for value in schedule):
        errors.append("every schedule value must use 24-hour HH:MM format")
    elif len(schedule) != len(set(schedule)):
        errors.append("schedule contains duplicate times")

    window = config.get("schedule_window_minutes")
    if not isinstance(window, int) or not 1 <= window <= 30:
        errors.append("schedule_window_minutes must be an integer from 1 to 30")

    maximum = config.get("max_candidates_per_account")
    if not isinstance(maximum, int) or not 1 <= maximum <= 20:
        errors.append("max_candidates_per_account must be an integer from 1 to 20")

    platforms = config.get("platforms")
    if not isinstance(platforms, list) or not platforms:
        errors.append("platforms must be a non-empty list")
    else:
        seen_accounts: set[str] = set()
        enabled_count = 0
        for platform_index, entry in enumerate(platforms):
            prefix = f"platforms[{platform_index}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be an object")
                continue
            platform = entry.get("platform")
            if not isinstance(platform, str) or not PLATFORM_PATTERN.fullmatch(platform):
                errors.append(f"{prefix}.platform must use lowercase letters, digits, and hyphens")
                platform = "invalid"
            accounts = entry.get("accounts")
            if not isinstance(accounts, list) or not accounts:
                errors.append(f"{prefix}.accounts must be a non-empty list")
                continue
            for account_index, account in enumerate(accounts):
                account_prefix = f"{prefix}.accounts[{account_index}]"
                if not isinstance(account, dict):
                    errors.append(f"{account_prefix} must be an object")
                    continue
                if not isinstance(account.get("name"), str) or not account["name"].strip():
                    errors.append(f"{account_prefix}.name is required")
                if not is_url(account.get("profile_url")):
                    errors.append(f"{account_prefix}.profile_url must be a complete http(s) URL")
                stable_id = account.get("stable_account_id")
                if not isinstance(stable_id, str) or not stable_id.strip():
                    errors.append(f"{account_prefix}.stable_account_id is required")
                    continue
                key = f"{platform}:{stable_id}"
                if key in seen_accounts:
                    errors.append(f"duplicate account identity: {key}")
                seen_accounts.add(key)
                if account.get("enabled", True):
                    enabled_count += 1
        if enabled_count == 0:
            warnings.append("all example accounts are disabled; enable at least one account before monitoring")

    lark = config.get("lark")
    if not isinstance(lark, dict):
        errors.append("lark must be an object")
    else:
        if not is_url(lark.get("base_url")):
            errors.append("lark.base_url must be a complete Base or Wiki http(s) URL")
        if not isinstance(lark.get("table_name"), str) or not lark["table_name"].strip():
            errors.append("lark.table_name is required")
        field_map = lark.get("field_map")
        if not isinstance(field_map, dict):
            errors.append("lark.field_map must be an object")
        else:
            missing = sorted(REQUIRED_FIELDS - field_map.keys())
            if missing:
                errors.append("lark.field_map is missing required logical keys: " + ", ".join(missing))
            values = [value for value in field_map.values() if isinstance(value, str)]
            if len(values) != len(field_map):
                errors.append("every lark.field_map value must be a field-name string")
            if len(values) != len(set(values)):
                errors.append("lark.field_map maps multiple logical keys to the same field")

    transcription = config.get("transcription")
    if not isinstance(transcription, dict):
        errors.append("transcription must be an object")
    elif transcription.get("enabled", True):
        for key in ("model", "language", "output_root"):
            if not isinstance(transcription.get(key), str) or not transcription[key].strip():
                errors.append(f"transcription.{key} is required when transcription is enabled")

    dangerous_keys = {"access_token", "refresh_token", "cookie", "cookies", "password", "secret"}
    serialized_keys = {str(key).lower() for key in walk_keys(config)}
    found = sorted(dangerous_keys & serialized_keys)
    if found:
        warnings.append("configuration contains sensitive-looking keys; keep the working file out of Git: " + ", ".join(found))

    return errors, warnings


def walk_keys(value: object):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid config: {exc}", file=sys.stderr)
        return 1

    errors, warnings = validate(config)
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("configuration is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
