#!/usr/bin/env python3
"""Tests for .claude/hooks/protect_kicad_v2.py with the repo's protect.json.

Run: python -I -X utf8 tools/tests/test_hook.py
Standard library only. The current-branch tests need `git` on PATH.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "protect_kicad_v2.py"
sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location("protect_hook", HOOK)
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)
RULES = hook.load_rules()


def decide(tool, cwd=None, **tool_input):
    """The hook's level for one tool call: 'deny', 'ask' or None."""
    result = hook.check({"tool_name": tool, "tool_input": tool_input, "cwd": cwd}, RULES)
    return result[0] if result else None


def bash(command, cwd=None):
    return decide("Bash", cwd=cwd, command=command)


def git_repo(tmp, branch):
    run = lambda *a: subprocess.run(["git", *a], cwd=tmp, check=True, capture_output=True)  # noqa: E731
    run("init", "-q")
    run("checkout", "-q", "-b", branch)
    run("-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "--allow-empty", "-m", "x")
    return tmp


class Edits(unittest.TestCase):
    def test_paths(self):
        self.assertEqual("ask", decide("Edit", file_path="hw/board.kicad_sch"))
        self.assertEqual("deny", decide("Write", file_path="hw/templates/a.md"))
        self.assertIsNone(decide("Edit", file_path="hw/library/0_IC.kicad_sym"))
        self.assertIsNone(decide("Edit", file_path="README.md"))

    def test_deny_before_allow(self):
        # deny > ask > allow: a denied glob wins inside an allowed folder
        self.assertEqual("deny", decide("Write", file_path="hw/library/3D/x.wrl"))
        self.assertEqual("ask", decide("Write", file_path="/tmp/scratchpad/t.kicad_sch"))

    def test_dotdot_cannot_hide(self):
        self.assertEqual("ask", decide("Edit", file_path="scratchpad/../hw/board.kicad_sch"))

    def test_shell_writes(self):
        self.assertEqual("ask", bash("sed -i 's/a/b/' hw/board.kicad_sch"))
        self.assertEqual("ask", bash("cd hw && rm board.KICAD_PCB"))
        self.assertIsNone(bash("cat hw/board.kicad_sch"))


class Pdf(unittest.TestCase):
    def test_read_tool(self):
        self.assertEqual("deny", decide("Read", file_path="D:\\p\\hw\\documents\\Schematics\\board.pdf"))
        self.assertEqual("deny", decide("Read", file_path="hw/documents/schematic/board.PDF"))
        self.assertEqual("deny", decide("Read", file_path="hw/documents/Manufacturing/fab.pdf"))
        self.assertEqual("ask", decide("Read", file_path="hw/datasheets/STM32H743.pdf"))
        self.assertIsNone(decide("Read", file_path="hw/documents/Reports/erc.pdf"))
        self.assertIsNone(decide("Read", file_path="C:/x/scratchpad/report.pdf"))
        self.assertIsNone(decide("Read", file_path="hw/notes.md"))

    def test_shell_reads(self):
        self.assertEqual("deny", bash("cat hw/documents/Schematics/x.PDF"))
        self.assertEqual("deny", bash("pdftotext hw/documents/schematic/board.pdf -"))
        self.assertEqual("ask", bash('python -c "open(\'ds/lm5164.pdf\',\'rb\').read()"'))
        self.assertEqual("ask", bash("bash -c 'pdftotext ds/a.pdf - | head'"))
        self.assertIsNone(bash("pdftotext hw/documents/reports/review.pdf -"))

    def test_shell_no_read(self):
        self.assertIsNone(bash("ls hw/documents/Schematics/*.pdf"))
        self.assertIsNone(bash("git add hw/documents/reports/r.pdf ds/a.pdf"))
        self.assertIsNone(bash("git log --stat -- ds/a.pdf"))
        self.assertEqual("ask", bash("git show HEAD:ds/a.pdf"))
        msg = "git commit -F - <<'EOF'\ndocs: cite ds/a.pdf by path\nEOF"
        self.assertIsNone(bash(msg))


class Git(unittest.TestCase):
    def test_push_protected(self):
        for c in ("git push origin main", "git push origin HEAD:main", "git push origin +main",
                  "git push origin dev:refs/heads/master", "git push -u origin main",
                  "git -C ../repo push origin main", "git push --all origin",
                  "git push --mirror", "git push origin :"):
            self.assertEqual("deny", bash(c), c)

    def test_force(self):
        for c in ("git push --force origin dev", "git push origin dev --force",
                  "git push -f origin dev", "git push origin -uf dev", "git push origin +dev"):
            self.assertEqual("deny", bash(c), c)
        self.assertEqual("ask", bash("git push --force-with-lease origin dev"))
        self.assertEqual("deny", bash("git push --force-with-lease origin main"))

    def test_delete_and_tags(self):
        for c in ("git push origin --delete feat/x", "git push origin -d feat/x",
                  "git push origin :feat/x", "git push --tags", "git push origin v1.0:refs/tags/v1.0"):
            self.assertEqual("ask", bash(c), c)

    def test_other_git(self):
        deny = ("git reset --hard HEAD~1", "git reset HEAD~1 --hard", "git clean -fd",
                "git clean -dfx", "git clean -d -f", "gh pr merge 12 --squash",
                "gh -R o/r pr merge 12", "gh api -X PUT repos/o/r/pulls/12/merge")
        for c in deny:
            self.assertEqual("deny", bash(c), c)
        ask = ("git branch -D feat/x", "git branch --delete feat/x", "git branch -d feat/x",
               "git branch -m old new", "git tag v1.0", "git tag -a v1.0 -m x",
               "git tag -d v1.0", "git rebase main", "git pull --rebase", "git commit --amend",
               "git commit -m x --amend", "gh release create v1.0")
        for c in ask:
            self.assertEqual("ask", bash(c), c)
        none = ("git status", "git log --oneline -5", "git branch -a", "git branch -vv",
                "git tag", "git tag -l 'v4*'", "git tag --sort=-v:refname", "git reset HEAD f.md",
                "git clean -n", "git commit -m 'fix: main push docs'", "gh pr create --base dev",
                "gh release view v1.0", "gh pr view 12", "git push origin feat/x",
                "git push -u origin dev")
        for c in none:
            self.assertIsNone(bash(c), c)

    def test_wrappers_and_chains(self):
        self.assertEqual("deny", bash("git status && git push origin main"))
        self.assertEqual("deny", bash("GIT_TRACE=1 git push origin main"))
        self.assertEqual("deny", bash('bash -c "git push origin main"'))
        self.assertEqual("deny", bash("git.exe push origin main"))
        self.assertEqual("ask", bash("git branch --merged | xargs -r git branch -d"))
        self.assertEqual("deny", decide("PowerShell", command="& git push origin main; echo ok"))

    def test_commit_message_text_is_not_a_command(self):
        msg = 'git commit -F - <<\'EOF\'\nfix: stop git push origin main\nEOF'
        self.assertIsNone(bash(msg))


@unittest.skipUnless(shutil.which("git"), "git not on PATH")
class CurrentBranch(unittest.TestCase):
    def test_push_without_refspec(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "a").mkdir()
            (Path(d) / "b").mkdir()
            main = git_repo(Path(d) / "a", "main")
            dev = git_repo(Path(d) / "b", "dev")
            self.assertEqual("deny", bash("git push", cwd=str(main)))
            self.assertEqual("deny", bash("git push origin HEAD", cwd=str(main)))
            self.assertEqual("deny", bash("git push --force-with-lease", cwd=str(main)))
            self.assertEqual("ask", bash("git push --force-with-lease", cwd=str(dev)))
            self.assertIsNone(bash("git push -u origin HEAD", cwd=str(dev)))
            # a cd earlier in the same command moves the lookup
            self.assertEqual("deny", bash(f'cd "{main}" && git push', cwd=str(dev)))
            self.assertIsNone(bash(f'cd "{dev}" && git push', cwd=str(main)))

    def test_unknown_branch_asks(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual("ask", bash("git push", cwd=d))


class Contract(unittest.TestCase):
    """Run the hook as Claude Code does: JSON on stdin, JSON on stdout."""

    def run_hook(self, event):
        out = subprocess.run([sys.executable, "-I", str(HOOK)], input=json.dumps(event),
                             capture_output=True, text=True, timeout=30)
        self.assertEqual(0, out.returncode, out.stderr)
        return json.loads(out.stdout)["hookSpecificOutput"] if out.stdout.strip() else None

    def test_deny_ask_none(self):
        res = self.run_hook({"tool_name": "Bash", "tool_input": {"command": "git push origin main"}})
        self.assertEqual("deny", res["permissionDecision"])
        self.assertIn("push-protected", res["permissionDecisionReason"])
        res = self.run_hook({"tool_name": "Read", "tool_input": {"file_path": "ds/a.pdf"}})
        self.assertEqual("ask", res["permissionDecision"])
        self.assertIn("rules/pdf.md", res["permissionDecisionReason"])
        self.assertIsNone(self.run_hook({"tool_name": "Read", "tool_input": {"file_path": "a.md"}}))

    def test_bad_input_fails_closed(self):
        res = self.run_hook({"tool_name": "Bash", "tool_input": "not a dict"})
        self.assertEqual("deny", res["permissionDecision"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
