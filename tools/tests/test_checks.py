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

HOOK_SRC = TOOLS.parent / ".claude" / "hooks" / "protect_kicad_v2.py"
PROTECT = {"deny": ["**/*.kicad_wks"], "ask": ["**/*.kicad_sch"], "allow": ["**/library/**"],
           "pdf": {"deny": ["**/documents/schematic*/**", "**/documents/manufacturing/**"],
                   "ask": [], "allow": ["**/documents/reports/**"]},
           "git": {"protected_branches": ["main"], "deny": ["push-protected"], "ask": ["tag"]}}
HOOK = {"PreToolUse": [{"matcher": "Edit|Write|MultiEdit|Read|Bash|PowerShell",
                        "hooks": [{"type": "command", "command": "python protect_kicad_v2.py"}]}]}


def project(tmp: Path, allow=(), ask=("Edit(**/*.kicad_sch)",), deny=("Edit(**/*.kicad_wks)",),
            hooks=HOOK, protect=PROTECT, mode="default"):
    (tmp / ".claude" / "hooks").mkdir(parents=True)
    perms = {"defaultMode": mode, "allow": list(allow), "ask": list(ask), "deny": list(deny)}
    (tmp / ".claude" / "settings.json").write_text(json.dumps({"permissions": perms, "hooks": hooks}))
    (tmp / ".claude" / "hooks" / "protect.json").write_text(json.dumps(protect))
    (tmp / ".claude" / "hooks" / "protect_kicad_v2.py").write_bytes(HOOK_SRC.read_bytes())
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

    def test_bypass_mode(self):
        self.assertTrue(any("bypassPermissions" in e for e in self.run_check(mode="bypassPermissions")))

    def test_schema(self):
        bad = json.loads(json.dumps(PROTECT))
        bad["git"]["ask"] = ["tag", "push-protected", "no-such-check"]
        bad["extra"] = 1
        errs = self.run_check(protect=bad)
        self.assertIn("protect.json git ask has unknown check 'no-such-check'", errs)
        self.assertIn("protect.json git check 'push-protected' is in both deny and ask", errs)
        self.assertIn("protect.json has an unknown key 'extra'", errs)
        nopdf = {k: v for k, v in PROTECT.items() if k != "pdf"}
        self.assertTrue(any("no 'pdf' block" in e for e in self.run_check(protect=nopdf)))

    def test_pdf_must_deny_both_spellings(self):
        weak = json.loads(json.dumps(PROTECT))
        weak["pdf"]["deny"] = ["**/documents/Schematics/**", "**/documents/manufacturing/**"]
        errs = self.run_check(protect=weak)
        self.assertTrue(any("hw/documents/schematic/board.pdf" in e for e in errs), errs)
        self.assertFalse(any("Schematics/board.pdf" in e for e in errs), errs)

    def test_repo_settings_pass(self):
        self.assertEqual([], cp.check(TOOLS.parent))


class Skills(unittest.TestCase):
    def test_frontmatter(self):
        fm = cs.frontmatter("---\nname: x\ndescription: >-\n  one\n  two\n---\nbody")
        self.assertEqual(fm["name"], "x")
        self.assertEqual(fm["description"], "one two")
        # A block marker with no text is an empty description.
        for marker in (">-", ">", "|", "|-"):
            self.assertEqual(cs.frontmatter(f"---\nname: x\ndescription: {marker}\n---\n")["description"], "")

    def test_global_skills_named_in_readme_must_exist(self):
        listed = {"kicad-naming", "kicad-typo"}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "kicad-naming").mkdir()
            (Path(d) / "kicad-naming" / "SKILL.md").write_text("x")
            self.assertEqual(cs.missing_global(listed, Path(d)), ["kicad-typo"])
            # Without the global folder (CI) nothing is checked.
            self.assertIsNone(cs.missing_global(listed, Path(d) / "absent"))

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
