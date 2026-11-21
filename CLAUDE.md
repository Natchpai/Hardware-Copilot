# CLAUDE.md

Guidance for Claude Code in this repository. Replace the two placeholder
sections below with your project's facts; everything else is the shared
Hardware-Copilot setup and can stay as it is.

## Project

<!-- One paragraph: what the board is, who owns it, KiCad version. -->
This repository holds a KiCad hardware project. The human engineer makes every
design and approval decision and declares the phase (DRAFT, PRELIMINARY,
CHECK, RELEASE). Read the phase from `README.md`; never infer it. Write files,
code, error messages, Git text and chat in English unless the user asks
otherwise.

## Layout

<!-- Paths Claude must know: the KiCad project folder, the root schematic and
     its sheet tree, library tables and prefixes, the design-record folder,
     the team-messages file (optional), anything generated from the records. -->
- Find the KiCad project first: the folder with the `.kicad_pro`. Its
  `fp-lib-table`, `sym-lib-table` and project libraries belong to the design.
- KiCad files are the **saved** design. A `~<project>.kicad_pro.lck` file
  means KiCad has the project open: read only the saved files, and say the
  editor may hold unsaved changes. `<project>-backups/` and `*.bak` are
  backups, not design sources.

## Rules

`.claude/rules/` loads every session and owns the rules:

- `engineering.md`: design authority, change proposals, evidence labels,
  datasheet sources.
- `workflow.md`: phases, Markdown docs, the spec, checklist and doc cycle,
  team messages, open checks.
- `pdf.md`: PDF reading and generation, and the datasheet fallback.
  `notebooklm.md`: NotebookLM procedure (path-scoped).
- `git-workflow.md`: hardware Git notes on top of the global
  `~/.claude/rules/git-workflow.md`, which holds the approval tiers. Every
  Git mutation needs explicit, action-specific approval in chat, even where
  `settings.json` lets the command run without a prompt.

This file adds:

- **Protected paths.** The `.claude/hooks/protect_kicad_v2.py` PreToolUse
  hook (rules in `.claude/hooks/protect.json`, order deny > ask > allow) and
  the permission lists in `.claude/settings.json` control edits to KiCad
  files, `library/` and `templates/`, PDF reads and risky Git commands;
  Hardware-Copilot `tools/check_permissions.py` checks that they agree. If the hook blocks or asks, report
  it; never edit the hook, `protect.json` or the permissions to get access,
  and do not work around a block with shell commands. A permission `allow` is
  not design authorization: a KiCad or library change still needs the
  engineer's approval of that specific change.
- **External-model providers** (`agent-coworker`: `agy` or `codex`): only
  when the user asks. Send them no PDFs, native KiCad files, `library/`
  contents, secrets or anything on the deny or ask lists. Hooks and
  `settings.json` do not apply inside a provider.
- Do not assume an optional tool, skill or script is installed; if one is
  missing, say so and do the step by hand or mark it `NOT_VERIFIED`.

## Tools

- **Library part:** `kicad-part-start`, then `kicad-link-audit` before the
  part is placed. Link fixes go through `/kicad-symbol-sync` or
  `/kicad-footprint-sync`, with approval. The `kicad-*` skills are global
  (see the Hardware-Copilot README, Libraries).
- **Design data:** `sch-inspect` and `pcb-inspect` extract evidence from the
  saved files; `sch-review` and `pcb-review` judge it. Query narrow targets
  (sheet, ref, net), and brief subagents the same way with exact paths.
  Unannotated refs such as `U?` return every match.
- **Docs:** the human runs `/progress-update` (design records); `hw-docs`
  keeps `README.md`, `CHANGELOG.md` and the phase line.
- **Datasheets:** NotebookLM by default, one notebook per part
  (`notebooklm list --json`).
- **Supplier data:** JLCPCB stock and price are JavaScript-rendered and Mouser
  often times out, so values from search snippets stay `NOT_VERIFIED`.
  Spot-check key values before writing them into a design record.

## Compact Instructions

When compacting, keep: requirement, decision and open-item IDs in play, files
changed and not yet committed, pending approvals and the exact change each
covers, evidence labels on open values, the branch and unpushed commits, and
decisions the user made this session. Do not carry over the phase; read it
from `README.md` again.
