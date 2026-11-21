#!/usr/bin/env python3
"""Tests for tools/sync_project.py with temporary git repositories.

Run: python -I -X utf8 tools/tests/test_sync_project.py
Standard library and git only.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
sys.dont_write_bytecode = True
import sync_project as sp  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def write(root, rel, text, crlf=False):
    f = Path(root) / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(text.replace("\n", "\r\n").encode() if crlf else text.encode())


class Sync(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.src, self.proj = base / "hc", base / "proj"
        self.src.mkdir()
        self.proj.mkdir()
        git(self.src, "init", "-q")
        git(self.src, "config", "user.email", "t@example.invalid")
        git(self.src, "config", "user.name", "t")
        git(self.src, "config", "core.autocrlf", "false")
        write(self.src, ".claude/skills/a/SKILL.md", "a1\n", crlf=True)
        write(self.src, ".claude/skills/gone/SKILL.md", "g1\n")
        write(self.src, ".claude/skills/git-workflow/SKILL.md", "gw\n")
        write(self.src, ".claude/rules/r.md", "r1\n")
        write(self.src, ".claude/hooks/h.py", "h1\n")
        write(self.src, ".claude/settings.json", json.dumps({"permissions": {"deny": ["X", "Y"]}}))
        write(self.src, ".claude-plugin/plugin.json", json.dumps({"version": "1.0.0"}))
        self.commit("v1.0.0")
        write(self.proj, ".claude/settings.json", json.dumps({"permissions": {"deny": ["X", "Z"]}}))
        write(self.proj, ".claude/skills/mine/SKILL.md", "project skill\n")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, tag):
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", tag)
        git(self.src, "tag", tag)

    def sync(self, apply=True, **kw):
        p = sp.plan(self.proj, self.src, **kw)
        if apply:
            sp.apply(p)
        return {path: action for action, path, _ in p["actions"]}, p

    def test_first_run_adds_and_keeps_project_files(self):
        acts, p = self.sync(exclude=("skills/git-workflow",))
        self.assertEqual(p["ref"], "v1.0.0")
        self.assertEqual(acts[".claude/skills/a/SKILL.md"], "add")
        self.assertEqual(acts[".claude/skills/mine/SKILL.md"], "local")
        self.assertNotIn(".claude/skills/git-workflow/SKILL.md", acts)
        self.assertNotIn(".claude/settings.json", acts)
        self.assertEqual((self.proj / ".claude/skills/a/SKILL.md").read_bytes(), b"a1\n")  # LF
        lock = json.loads((self.proj / sp.LOCK).read_text())
        self.assertEqual((lock["ref"], lock["version"], lock["exclude"]), ("v1.0.0", "1.0.0", ["skills/git-workflow"]))
        self.assertIn(".claude/hooks/h.py", lock["files"])
        self.assertEqual(json.loads((self.proj / ".claude/settings.json").read_text())["permissions"]["deny"], ["X", "Z"])
        self.assertEqual(p["settings"], {"upstream_only_deny": ["Y"], "project_only_deny": ["Z"]})
        # second run: nothing to do; the exclude is remembered from the lock
        acts, _ = self.sync()
        self.assertEqual({a for a in acts.values()}, {"same", "local"})

    def test_update_keep_overwrite_remove(self):
        self.sync()
        write(self.src, ".claude/skills/a/SKILL.md", "a2\n")
        write(self.src, ".claude/rules/r.md", "r2\n")
        (self.src / ".claude/skills/gone/SKILL.md").unlink()
        self.commit("v1.1.0")
        write(self.proj, ".claude/rules/r.md", "r1 local edit\n")
        acts, _ = self.sync(apply=False)
        self.assertEqual(acts[".claude/skills/a/SKILL.md"], "update")
        self.assertEqual(acts[".claude/rules/r.md"], "keep")
        self.assertEqual(acts[".claude/skills/gone/SKILL.md"], "remove")
        self.sync()
        self.assertEqual((self.proj / ".claude/skills/a/SKILL.md").read_text(), "a2\n")
        self.assertEqual((self.proj / ".claude/rules/r.md").read_text(), "r1 local edit\n")
        self.assertFalse((self.proj / ".claude/skills/gone").exists())  # empty folder removed
        acts, _ = self.sync(overwrite=(".claude/rules/r.md",))
        self.assertEqual(acts[".claude/rules/r.md"], "update")
        self.assertEqual((self.proj / ".claude/rules/r.md").read_text(), "r2\n")

    def test_first_run_never_overwrites_a_differing_file(self):
        write(self.proj, ".claude/rules/r.md", "older copy\n")
        acts, _ = self.sync()
        self.assertEqual(acts[".claude/rules/r.md"], "keep")
        self.assertEqual((self.proj / ".claude/rules/r.md").read_text(), "older copy\n")
        self.assertNotIn(".claude/rules/r.md", json.loads((self.proj / sp.LOCK).read_text())["files"])

    def test_baseline_adopts_a_hand_copy(self):
        # The project was copied from v1.0.0 by hand, then v1.1.0 changed a and dropped gone.
        for rel in (".claude/skills/a/SKILL.md", ".claude/skills/gone/SKILL.md", ".claude/rules/r.md"):
            write(self.proj, rel, (self.src / rel).read_bytes().decode())
        write(self.proj, ".claude/hooks/h.py", "h1 edited\n")
        write(self.src, ".claude/skills/a/SKILL.md", "a2\n")
        (self.src / ".claude/skills/gone/SKILL.md").unlink()
        self.commit("v1.1.0")
        acts, _ = self.sync(apply=False, baseline="v1.0.0")
        self.assertEqual(acts[".claude/skills/a/SKILL.md"], "update")
        self.assertEqual(acts[".claude/skills/gone/SKILL.md"], "remove")
        self.assertEqual(acts[".claude/hooks/h.py"], "keep")       # edited: not like v1.0.0
        self.assertEqual(acts[".claude/skills/mine/SKILL.md"], "local")
        self.sync(baseline="v1.0.0")
        with self.assertRaises(sp.SyncError):                         # only for the first sync
            sp.plan(self.proj, self.src, baseline="v1.0.0")

    def test_dry_run_writes_nothing(self):
        before = sorted(p.relative_to(self.proj).as_posix() for p in self.proj.rglob("*"))
        self.sync(apply=False)
        self.assertEqual(sorted(p.relative_to(self.proj).as_posix() for p in self.proj.rglob("*")), before)

    def test_refuses_own_clone(self):
        with self.assertRaises(sp.SyncError):
            sp.plan(self.src, self.src)


if __name__ == "__main__":
    unittest.main(verbosity=1)
