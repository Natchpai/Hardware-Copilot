#!/usr/bin/env python3
"""Check a project's .claude/settings.json and .claude/hooks/protect.json.

Read-only. Python 3.10+ standard library only. Exit 1 on any failure.

    python -I tools/check_permissions.py [<project root>]

The hook (protect_kicad_v2.py) guards edits, PDF reads and Git commands with
protect.json; settings.json gives Claude Code's own prompts. Both are edited
by hand and can drift. The checks:
- protect.json has the expected shape: path lists, a `pdf` block, and a `git`
  block whose names the project's hook knows, none in both deny and ask;
- the `pdf` block denies schematic and manufacturing PDFs in both folder
  spellings (`rules/pdf.md`), tested with the hook's own matcher;
- every protect.json deny glob is an `Edit(...)` deny in settings.json, and
  every ask glob an `Edit(...)` ask;
- settings.json does not allow, by an `Edit(...)` rule, a glob the hook denies
  or asks for, and does not deny or ask for a glob the hook allows;
- settings.json does not run in bypassPermissions mode, which skips the asks;
- the PreToolUse hook entry runs protect_kicad_v2.py for Edit, Write, Read
  and Bash.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HOOK_TOOLS = ("Edit", "Write", "Read", "Bash")
PDF_MUST_DENY = [
    "hw/documents/schematic/board.pdf",
    "hw/documents/Schematics/board.pdf",
    "hw/documents/manufacturing/fab.pdf",
    "hw/documents/Manufacturing/fab.pdf",
]
TOP_KEYS = {"_help", "deny", "ask", "allow", "pdf", "git"}
EDIT_RE = re.compile(r"^Edit\((.+)\)$")
VERB = {"deny": "denies", "ask": "asks for"}


def edit_globs(rules: list[str]) -> set[str]:
    return {m.group(1).lower() for r in rules if (m := EDIT_RE.match(r))}


def load_hook(root: Path):
    path = root / ".claude" / "hooks" / "protect_kicad_v2.py"
    sys.dont_write_bytecode = True             # no __pycache__ in the project's hooks
    spec = importlib.util.spec_from_file_location("protect_hook", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def is_str_list(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def check_schema(protect: dict, hook) -> list[str]:
    errors = []
    for k in sorted(set(protect) - TOP_KEYS):
        errors.append(f"protect.json has an unknown key '{k}'")
    for k in ("deny", "ask", "allow"):
        if not is_str_list(protect.get(k, [])):
            errors.append(f"protect.json '{k}' must be a list of globs")
    pdf = protect.get("pdf")
    if not isinstance(pdf, dict):
        errors.append("protect.json has no 'pdf' block (rules/pdf.md)")
    else:
        for k in ("deny", "ask", "allow"):
            if not is_str_list(pdf.get(k, [])):
                errors.append(f"protect.json pdf '{k}' must be a list of globs")
    git = protect.get("git")
    if not isinstance(git, dict):
        errors.append("protect.json has no 'git' block")
        return errors
    names = {}
    for k in ("deny", "ask"):
        v = git.get(k, [])
        if not is_str_list(v):
            errors.append(f"protect.json git '{k}' must be a list of check names")
            continue
        names[k] = set(v)
        for n in sorted(set(v) - set(hook.GIT_CHECKS)):
            errors.append(f"protect.json git {k} has unknown check '{n}'")
    for n in sorted(names.get("deny", set()) & names.get("ask", set())):
        errors.append(f"protect.json git check '{n}' is in both deny and ask")
    if not is_str_list(git.get("protected_branches", [])) or not git.get("protected_branches"):
        errors.append("protect.json git 'protected_branches' must be a non-empty list")
    return errors


def check(root: Path) -> list[str]:
    settings = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
    protect = json.loads((root / ".claude" / "hooks" / "protect.json").read_text(encoding="utf-8"))
    hook = load_hook(root)
    errors = check_schema(protect, hook)
    if not errors:
        rules = hook.load_rules(root / ".claude" / "hooks" / "protect.json")
        for p in PDF_MUST_DENY:
            level, _ = hook.classify(p, rules["pdf"], default="ask")
            if level != "deny":
                errors.append(f"protect.json pdf block gives '{level}' for {p}; it must deny "
                              "schematic and manufacturing PDFs (rules/pdf.md)")
    perms = settings.get("permissions", {})
    s = {k: edit_globs(perms.get(k, [])) for k in ("allow", "ask", "deny")}
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
    if perms.get("defaultMode") == "bypassPermissions":
        errors.append("settings.json defaultMode bypassPermissions skips the hook's asks")
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
    except (OSError, ValueError, ImportError, AttributeError, SyntaxError) as exc:
        print(f"FAIL cannot read settings, protect.json or the hook: {exc}")
        return 1
    for e in errors:
        print(f"FAIL {e}")
    print(f"check_permissions: {root.name}: {len(errors)} failures")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
