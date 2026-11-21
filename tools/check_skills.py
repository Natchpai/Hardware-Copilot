#!/usr/bin/env python3
"""Check the skills in .claude/skills against the shared rules.

Read-only by default. Python 3.10+ standard library only. Exit 1 on any
failure. Checks:
- every SKILL.md has frontmatter with `name` (equal to its folder) and
  `description`;
- every skill except those in NO_BASELINE carries the block in
  shared/evidence-baseline.md word for word (one copy, so skills still work
  when copied alone, but they cannot drift);
- every skill is named in the README skill tables, and every skill named
  there exists.

    python -I tools/check_skills.py [--fix]

--fix rewrites the `## Evidence baseline` section of each skill to the shared
block (or inserts it before the first `## ` heading). Nothing else is changed.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"
BASELINE = ROOT / "shared" / "evidence-baseline.md"
README = ROOT / "README.md"
NO_BASELINE = {"git-workflow"}  # Git only; follows the Git rules instead
GLOBAL_SKILLS = re.compile(r"^kicad-")  # README group 5 lists global skills kept elsewhere
SECTION_RE = re.compile(r"(?ms)^## Evidence baseline\n.*?(?=^## |\Z)")


def frontmatter(text: str) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    if not m:
        return {}
    out, key = {}, None
    for ln in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", ln)
        if km:
            key = km.group(1)
            out[key] = km.group(2).strip()
        elif key and ln.startswith(" "):
            out[key] = (out[key] + " " + ln.strip()).strip()
    return out


def with_baseline(text: str, block: str) -> str:
    block = block.rstrip("\n") + "\n\n"
    if SECTION_RE.search(text):
        return SECTION_RE.sub(lambda _: block, text, count=1)
    m = re.search(r"(?m)^## ", text)
    return text[:m.start()] + block + text[m.start():] if m else text.rstrip("\n") + "\n\n" + block


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fix", action="store_true", help="write the shared baseline into each skill")
    args = ap.parse_args()
    block = BASELINE.read_text(encoding="utf-8").replace("\r\n", "\n")
    errors = []
    names = sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    for name in names:
        path = SKILLS / name / "SKILL.md"
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        fm = frontmatter(text)
        if fm.get("name") != name:
            errors.append(f"{name}: frontmatter name is {fm.get('name')!r}")
        if not fm.get("description"):
            errors.append(f"{name}: frontmatter has no description")
        if name in NO_BASELINE:
            continue
        if args.fix:
            new = with_baseline(text, block)
            if new != text:
                path.write_text(new, encoding="utf-8", newline="\n")
                print(f"fixed: {name}")
            text = new
        sections = SECTION_RE.findall(text)
        if len(sections) != 1:
            errors.append(f"{name}: {len(sections)} '## Evidence baseline' sections (need 1)")
        elif sections[0].rstrip("\n") != block.rstrip("\n"):
            errors.append(f"{name}: evidence baseline differs from shared/evidence-baseline.md")
    readme = README.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Skills\n(.*?)(?=^## |\Z)", readme)
    listed = set(re.findall(r"(?m)^\|\s*`([a-z0-9-]+)`\s*\|", m.group(1) if m else ""))
    if not m:
        errors.append("README.md has no '## Skills' section")
    for name in names:
        if name not in listed:
            errors.append(f"{name}: not in the README skill tables")
    for name in sorted(listed - set(names)):
        if not GLOBAL_SKILLS.match(name):
            errors.append(f"{name}: in the README skill tables but not in .claude/skills")
    for e in errors:
        print(f"FAIL {e}")
    print(f"check_skills: {len(names)} skills, {len(errors)} failures")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
