# Contributing to Hardware-Copilot

Thanks for helping. This repo holds Claude Code skills, rules and a file guard for KiCad 10 hardware work. Bug reports, fixes and new skills are welcome.

## Report a bug or ask a question

Open a [GitHub Issue](https://github.com/Natchpai/Hardware-Copilot/issues). Include:

- the skill and command you ran, and what you expected
- the KiCad version that saved the file, and your OS and Python version
- the smallest example that shows the problem

Do not attach design files you cannot share. A short excerpt of the S-expression is usually enough.

## Set up

- Python 3.10 or later. The scripts use the standard library only, so there is nothing to install.
- Claude Code, to try skills in a real session.

## Run the tests

From the repository root:

```sh
python -m unittest discover -s .claude/skills/sch-inspect/tests -p 'test_query_sch.py' -v
python -m unittest discover -s .claude/skills/pcb-inspect/tests -p 'test_query_pcb.py' -v
```

Golden tests use real KiCad projects that are not in the repo. They are opt-in and skip when no project is set. See [Tests and CI](README.md#tests-and-ci).

Add or update a synthetic test before you fix a confirmed bug in a parser.

## Make a change

1. Fork the repo and branch from `dev`.
2. Keep the change small and focused on one thing.
3. Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages and the PR title, for example `fix(sch-inspect): handle empty sheet`.
4. Open a pull request against `dev` and fill in the [PR template](.github/pull_request_template.md).
5. For a release, bump `version` in `.claude-plugin/plugin.json` so plugin users get the update.

## Project rules

Changes must keep the rules in [CLAUDE.md](CLAUDE.md) and [.claude/rules/](.claude/rules/):

- Skills never read datasheet, schematic or PCB PDFs. Datasheet values come from NotebookLM (default), the user or official web pages. PDF rules are in `.claude/rules/pdf.md`.
- Inspection and review skills treat KiCad design and library files as read-only.
- Findings carry evidence labels (`VERIFIED`, `ASSUMED`, `ESTIMATED`, `NOT_VERIFIED`).
- Each skill stays self-contained: it works when copied alone.
- Write in simple, direct English. Do not use the em dash.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By taking part, you agree to follow it.
