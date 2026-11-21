#!/usr/bin/env python3
"""Check that .claude/settings.json agrees with .claude/hooks/protect.json.

Read-only. Python 3.10+ standard library only. Exit 1 on any failure.

    python -I tools/check_permissions.py [<project root>]

The hook (protect_kicad_v2.py) guards edits with protect.json; settings.json
gives Claude Code's own prompts. They are edited by hand and can drift. The
checks:
- every protect.json deny glob is an `Edit(...)` deny in settings.json, and
  every ask glob an `Edit(...)` ask;
- settings.json does not allow, by an `Edit(...)` rule, a glob the hook denies
  or asks for, and does not deny or ask for a glob the hook allows;
- the PDF reads that `rules/pdf.md` forbids are denied, in both folder
  spellings (`schematic`/`Schematics`, `manufacturing`/`Manufacturing`);
- the PreToolUse hook entry runs protect_kicad_v2.py for Edit, Write and Bash.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_DENY = [
    "Read(**/documents/schematic/**/*.pdf)",
    "Read(**/documents/Schematics/**/*.pdf)",
    "Read(**/documents/manufacturing/**/*.pdf)",
    "Read(**/documents/Manufacturing/**/*.pdf)",
]
HOOK_TOOLS = ("Edit", "Write", "Bash")
EDIT_RE = re.compile(r"^Edit\((.+)\)$")
VERB = {"deny": "denies", "ask": "asks for"}


def edit_globs(rules: list[str]) -> set[str]:
    return {m.group(1).lower() for r in rules if (m := EDIT_RE.match(r))}


def check(root: Path) -> list[str]:
    settings = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
    protect = json.loads((root / ".claude" / "hooks" / "protect.json").read_text(encoding="utf-8"))
    perms = settings.get("permissions", {})
    s = {k: edit_globs(perms.get(k, [])) for k in ("allow", "ask", "deny")}
    errors = []
    for level in ("deny", "ask"):
        for g in protect.get(level, []):
            if g.lower() not in s[level]:
                errors.append(f"protect.json {level} '{g}' has no Edit({g}) {level} rule in settings.json")
            if g.lower() in s["allow"]:
                errors.append(f"settings.json allows Edit({g}), which protect.json {VERB[level]}")
    for g in protect.get("allow", []):
        for level in ("deny", "ask"):
            if g.lower() in s[level]:
                errors.append(f"settings.json {VERB[level]} Edit({g}), which protect.json allows")
    deny = set(perms.get("deny", []))
    for r in REQUIRED_DENY:
        if r not in deny:
            errors.append(f"settings.json deny is missing {r} (rules/pdf.md)")
    entries = settings.get("hooks", {}).get("PreToolUse", [])
    hooked = [e for e in entries
              if any("protect_kicad_v2.py" in h.get("command", "") for h in e.get("hooks", []))]
    if not hooked:
        errors.append("settings.json has no PreToolUse hook that runs protect_kicad_v2.py")
    else:
        tools = set(re.split(r"\|", hooked[0].get("matcher", "")))
        missing = [t for t in HOOK_TOOLS if t not in tools]
        if missing:
            errors.append(f"protect_kicad_v2.py hook matcher lacks {missing}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    try:
        errors = check(root)
    except (OSError, ValueError) as exc:
        print(f"FAIL cannot read settings: {exc}")
        return 1
    for e in errors:
        print(f"FAIL {e}")
    print(f"check_permissions: {root.name}: {len(errors)} failures")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
