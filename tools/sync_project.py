#!/usr/bin/env python3
"""Sync Hardware-Copilot skills, rules and hooks into a KiCad project.

Python 3.10+ standard library only. Dry run by default: it prints the plan and
writes nothing until --apply is given.

    python -I tools/sync_project.py <project root> [--ref vX.Y.Z] [--apply]
        [--baseline vX.Y.Z] [--overwrite PATH ...] [--exclude PATH ...] [--json]

What it does:
- Reads `.claude/skills/`, `.claude/rules/` and `.claude/hooks/` from this
  Hardware-Copilot clone at a git ref (default: the newest version tag), with
  `git show`, so a dirty working tree is never copied. Text files are
  written with LF line endings.
- Never touches `.claude/settings.json`, `settings.local.json`, `memory/` or
  `__pycache__`. For settings.json it prints what upstream has that the
  project lacks (and the reverse); you merge that by hand.
- Keeps `.claude/hardware-copilot.lock.json` in the project: the ref, the
  version, the excluded paths and the sha256 of every file it wrote. With it:
  - a file unchanged since the last sync is updated or, when gone upstream,
    removed;
  - a file edited in the project is kept and reported, unless named with
    --overwrite;
  - a file the lock does not know (a project's own skill, or any differing
    file on the first run) is never overwritten or removed without
    --overwrite.
- --exclude takes paths relative to `.claude/` (for example
  `skills/git-workflow`); they are stored in the lock and skipped from then on.
- --baseline vX.Y.Z is for the first sync of a project copied by hand: files
  equal to that release count as synced from it, so they update, or leave
  when the release dropped them. Other differing files are still kept.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

SOURCE = Path(__file__).resolve().parents[1]
SYNCED = (".claude/skills", ".claude/rules", ".claude/hooks")
NEVER = (".claude/settings.json", ".claude/settings.local.json")
NEVER_PARTS = ("memory", "__pycache__")
LOCK = ".claude/hardware-copilot.lock.json"


class SyncError(Exception):
    pass


def git(repo: Path, *args: str, binary: bool = False):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if proc.returncode:
        raise SyncError(f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout if binary else proc.stdout.decode("utf-8")


def default_ref(source: Path) -> str:
    tags = [t for t in git(source, "tag", "--sort=-v:refname").split() if t.startswith("v")]
    if not tags:
        raise SyncError("no version tag in the Hardware-Copilot clone; pass --ref")
    return tags[0]


def normalize(data: bytes) -> bytes:
    """LF line endings for text; binary (has a NUL byte) unchanged."""
    return data if b"\0" in data else data.replace(b"\r\n", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(normalize(data)).hexdigest()


def skipped(path: str, exclude: list[str]) -> bool:
    p = PurePosixPath(path)
    if path in NEVER or any(part in NEVER_PARTS for part in p.parts):
        return True
    rel = PurePosixPath(*p.parts[1:]) if p.parts[:1] == (".claude",) else p
    return any(rel == PurePosixPath(e) or PurePosixPath(e) in rel.parents for e in exclude)


def upstream_files(source: Path, ref: str, exclude: list[str]) -> dict[str, bytes]:
    names = git(source, "ls-tree", "-r", "--name-only", ref, "--", *SYNCED).splitlines()
    return {n: normalize(git(source, "show", f"{ref}:{n}", binary=True)) for n in names if not skipped(n, exclude)}


def upstream_version(source: Path, ref: str) -> str | None:
    try:
        return json.loads(git(source, "show", f"{ref}:.claude-plugin/plugin.json")).get("version")
    except (SyncError, ValueError):
        return None


def local_files(project: Path, exclude: list[str]) -> dict[str, bytes]:
    out = {}
    for top in SYNCED:
        base = project / top
        if base.is_dir():
            for f in base.rglob("*"):
                rel = f.relative_to(project).as_posix()
                if f.is_file() and not skipped(rel, exclude):
                    out[rel] = f.read_bytes()
    return out


def plan(project: Path, source: Path = SOURCE, ref: str | None = None,
         overwrite: tuple = (), exclude: tuple = (), baseline: str | None = None) -> dict:
    project = project.resolve()
    if project == source.resolve():
        raise SyncError("the project root is the Hardware-Copilot clone itself")
    if not project.is_dir():
        raise SyncError(f"project root not found: {project}")
    lock_path = project / LOCK
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.is_file() else {}
    excl = sorted(set(lock.get("exclude", [])) | set(exclude))
    ref = ref or default_ref(source)
    up = upstream_files(source, ref, excl)
    local = local_files(project, excl)
    known = lock.get("files", {})
    if not lock and baseline:
        # First sync of a project copied by hand: files equal to the release it
        # was copied from count as synced from that release.
        known = {path: sha(data) for path, data in upstream_files(source, baseline, excl).items()
                 if path in local and sha(local[path]) == sha(data)}
    elif lock and baseline:
        raise SyncError("--baseline is only for the first sync; this project already has a lock")
    over = {PurePosixPath(o).as_posix() for o in overwrite}
    actions = []
    for path in sorted(set(up) | set(local) | set(known)):
        if skipped(path, excl):
            continue
        u, l = up.get(path), local.get(path)
        if u is not None and l is None:
            actions.append(("add", path, "new upstream" if path not in known else "missing in project"))
        elif u is not None and sha(l) == sha(u):
            actions.append(("same", path, ""))
        elif u is not None:
            if path in over:
                actions.append(("update", path, "--overwrite"))
            elif path in known and sha(l) == known[path]:
                actions.append(("update", path, "changed upstream"))
            elif path in known:
                actions.append(("keep", path, "edited in the project; --overwrite to replace"))
            else:
                actions.append(("keep", path, "differs and not in the lock; --overwrite to replace"))
        elif l is not None and path in known:
            if sha(l) == known[path] or path in over:
                actions.append(("remove", path, "gone upstream"))
            else:
                actions.append(("keep", path, "gone upstream but edited in the project"))
        elif l is not None:
            actions.append(("local", path, "project file, not from Hardware-Copilot"))
    return {"project": str(project), "source": str(source), "ref": ref,
            "commit": git(source, "rev-parse", f"{ref}^{{commit}}").strip(),
            "version": upstream_version(source, ref), "exclude": excl,
            "actions": actions, "upstream": up, "lock": lock,
            "settings": settings_diff(project, source, ref)}


def settings_diff(project: Path, source: Path, ref: str) -> dict:
    try:
        up = json.loads(git(source, "show", f"{ref}:.claude/settings.json"))
    except (SyncError, ValueError):
        return {"note": "no upstream settings.json"}
    f = project / ".claude" / "settings.json"
    if not f.is_file():
        return {"note": "project has no .claude/settings.json; copy the upstream one by hand if wanted"}
    try:
        loc = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as exc:
        return {"note": f"project settings.json is not valid JSON: {exc}"}
    out = {}
    for level in ("allow", "ask", "deny"):
        a = set(up.get("permissions", {}).get(level, []))
        b = set(loc.get("permissions", {}).get(level, []))
        if a - b:
            out[f"upstream_only_{level}"] = sorted(a - b)
        if b - a:
            out[f"project_only_{level}"] = sorted(b - a)
    if up.get("hooks") != loc.get("hooks"):
        out["hooks"] = "differs from upstream"
    return out


def apply(p: dict) -> None:
    project = Path(p["project"])
    files = dict(p["lock"].get("files", {}))
    for action, path, _ in p["actions"]:
        target = project / path
        if action in ("add", "update"):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(p["upstream"][path])
            files[path] = sha(p["upstream"][path])
        elif action == "same":
            files[path] = sha(p["upstream"][path])
        elif action == "remove":
            target.unlink()
            files.pop(path, None)
            parent = target.parent
            while parent != project and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
    lock = {"source": "Hardware-Copilot", "ref": p["ref"], "commit": p["commit"], "version": p["version"],
            "exclude": p["exclude"], "files": dict(sorted(files.items()))}
    (project / LOCK).write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8", newline="\n")


def report(p: dict, applied: bool) -> str:
    counts: dict = {}
    lines = [f"Hardware-Copilot {p['ref']} ({p['commit'][:7]}, version {p['version']}) -> {p['project']}"]
    if p["exclude"]:
        lines.append(f"excluded: {', '.join(p['exclude'])}")
    for action, path, why in p["actions"]:
        counts[action] = counts.get(action, 0) + 1
        if action != "same":
            lines.append(f"  {action:<6} {path}" + (f"  ({why})" if why else ""))
    lines.append("summary: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    if p["settings"]:
        lines.append("settings.json (not changed; merge by hand):")
        for k, v in p["settings"].items():
            lines.append(f"  {k}: {v}")
    lines.append(f"lock written: {LOCK}" if applied else "dry run: nothing written; pass --apply to write")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", help="project repository root (the folder that holds .claude/)")
    ap.add_argument("--ref", help="Hardware-Copilot git ref; default: newest version tag")
    ap.add_argument("--apply", action="store_true", help="write the files and the lock")
    ap.add_argument("--overwrite", action="append", default=[], metavar="PATH",
                    help="replace this file even if edited in the project (path from the project root)")
    ap.add_argument("--exclude", action="append", default=[], metavar="PATH",
                    help="skip this path under .claude/ from now on, for example skills/git-workflow")
    ap.add_argument("--baseline", metavar="REF",
                    help="first sync only: the Hardware-Copilot release the project was copied from by hand")
    ap.add_argument("--json", action="store_true", help="print the plan as JSON")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        p = plan(Path(args.project), SOURCE, args.ref, tuple(args.overwrite), tuple(args.exclude), args.baseline)
        if args.apply:
            apply(p)
    except (SyncError, OSError, ValueError) as exc:
        print(f"sync_project: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({k: v for k, v in p.items() if k not in ("upstream", "lock")}, indent=1))
    else:
        print(report(p, args.apply))
    return 0


if __name__ == "__main__":
    sys.exit(main())
