#!/usr/bin/env python3
"""Tests for tools/check_skills.py and tools/check_permissions.py.

Run: python -I -X utf8 tools/tests/test_checks.py
Standard library only.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
sys.dont_write_bytecode = True
import check_permissions as cp  # noqa: E402
import check_skills as cs  # noqa: E402

PROTECT = {"deny": ["**/*.kicad_wks"], "ask": ["**/*.kicad_sch"], "allow": ["**/library/**"]}
HOOK = {"PreToolUse": [{"matcher": "Edit|Write|MultiEdit|Bash|PowerShell",
                        "hooks": [{"type": "command", "command": "python protect_kicad_v2.py"}]}]}


def project(tmp: Path, allow=(), ask=("Edit(**/*.kicad_sch)",), deny=("Edit(**/*.kicad_wks)",), hooks=HOOK):
    (tmp / ".claude" / "hooks").mkdir(parents=True)
    perms = {"allow": list(allow), "ask": list(ask), "deny": list(deny) + cp.REQUIRED_DENY}
    (tmp / ".claude" / "settings.json").write_text(json.dumps({"permissions": perms, "hooks": hooks}))
    (tmp / ".claude" / "hooks" / "protect.json").write_text(json.dumps(PROTECT))
    return tmp


class Permissions(unittest.TestCase):
    def run_check(self, **kw):
        with tempfile.TemporaryDirectory() as d:
            return cp.check(project(Path(d), **kw))

    def test_consistent(self):
        self.assertEqual([], self.run_check())

    def test_missing_and_weakened(self):
        errs = self.run_check(ask=(), allow=("Edit(**/*.kicad_sch)",))
        self.assertTrue(any("has no Edit(**/*.kicad_sch) ask" in e for e in errs))
        self.assertTrue(any("settings.json allows Edit(**/*.kicad_sch)" in e for e in errs))

    def test_denies_hook_allow(self):
        errs = self.run_check(deny=("Edit(**/*.kicad_wks)", "Edit(**/library/**)"))
        self.assertIn("settings.json denies Edit(**/library/**), which protect.json allows", errs)

    def test_hook_entry(self):
        self.assertTrue(any("no PreToolUse hook" in e for e in self.run_check(hooks={})))
        bad = {"PreToolUse": [{"matcher": "Edit", "hooks": [{"command": "python protect_kicad_v2.py"}]}]}
        self.assertTrue(any("matcher lacks" in e for e in self.run_check(hooks=bad)))


class Skills(unittest.TestCase):
    def test_frontmatter(self):
        fm = cs.frontmatter("---\nname: x\ndescription: >-\n  one\n  two\n---\nbody")
        self.assertEqual(fm["name"], "x")
        self.assertEqual(fm["description"], ">- one two")

    def test_with_baseline_insert_and_replace(self):
        block = "## Evidence baseline\n\n- rule\n"
        text = "---\nname: x\n---\n\n# X\n\nIntro.\n\n## Steps\n\n1. a\n"
        once = cs.with_baseline(text, block)
        self.assertIn("Intro.\n\n## Evidence baseline\n\n- rule\n\n## Steps", once)
        self.assertEqual(once, cs.with_baseline(once, block))  # stable
        drifted = once.replace("- rule", "- old rule")
        self.assertEqual(once, cs.with_baseline(drifted, block))

    def test_repo_skills_pass(self):
        sys.argv = ["check_skills.py"]
        self.assertEqual(0, cs.main())


if __name__ == "__main__":
    unittest.main(verbosity=1)
