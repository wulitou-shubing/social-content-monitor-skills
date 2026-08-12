#!/usr/bin/env python3
"""Validate the repository's Agent Skill structure without third-party packages."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: missing opening YAML delimiter")

    try:
        closing = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: missing closing YAML delimiter") from exc

    values: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}: unsupported frontmatter line {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key not in ALLOWED_FRONTMATTER_KEYS:
            raise ValueError(f"{path}: unsupported frontmatter key {key!r}")
        if not value:
            raise ValueError(f"{path}: empty frontmatter value for {key!r}")
        values[key] = value

    missing = ALLOWED_FRONTMATTER_KEYS - values.keys()
    if missing:
        raise ValueError(f"{path}: missing frontmatter keys {sorted(missing)}")
    return values


def validate_skill(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    values = parse_frontmatter(skill_file)
    name = values["name"]
    if name != skill_dir.name:
        raise ValueError(f"{skill_file}: name must match parent folder")
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        raise ValueError(f"{skill_file}: invalid skill name {name!r}")
    if len(values["description"]) > 1024:
        raise ValueError(f"{skill_file}: description exceeds 1024 characters")
    if not (skill_dir / "agents" / "openai.yaml").is_file():
        raise ValueError(f"{skill_dir}: missing agents/openai.yaml")


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        raise ValueError("no Skill folders found")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir)
        print(f"valid: {skill_dir.name}")
    print(f"validated {len(skill_dirs)} Skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
