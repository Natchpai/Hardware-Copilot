## Hardware Design Project

This repository contains a hardware engineering project. Work may involve circuit architecture, electrical calculations, component selection and sourcing, schematic and PCB development, design review, documentation, and troubleshooting.

Assist with the engineering task at hand. Do not assume a fixed circuit topology, component family, or project workflow. The human engineer makes final design and approval decisions.

## Project Context

- Use the project's requirements, existing design files, and documentation to understand the current design before making recommendations.
- Locate the KiCad project first: the folder with the `.kicad_pro` file. Its library tables (`fp-lib-table`, `sym-lib-table`) and project-local libraries belong to the design.
- Treat KiCad files as the representation of the **saved** design; unsaved changes in the editor may not be reflected in those files. A `~<project>.kicad_pro.lck` file means KiCad has the project open: read only the saved files, and say the editor may hold unsaved changes.
- `<project>-backups/` and `*.bak` are KiCad backups, not design sources.
- The human engineer declares the phase (DRAFT, PRELIMINARY, CHECK, RELEASE). Read it from `README.md`; never infer it.
- Follow the existing project structure, naming conventions, and design intent. Do not introduce new conventions without a clear need.
- Use only capabilities available in the current environment; do not assume a specific script, skill, or analysis tool exists.

## Protected Files

Native design files and local libraries are protected by the `.claude/hooks/protect_kicad_v2.py` hook. The rules live in `.claude/hooks/protect.json`, and `.claude/settings.json` should stay consistent with them.

- **Default:** inspect and propose changes with justification; do not edit.
- If the hook blocks or asks, report it. Never edit the hook, `protect.json`, or permission settings to gain access, and do not bypass a block with shell commands.
- The engineer edits `protect.json` (order allow > deny > ask) and `settings.json`, and the two can disagree: one may allow what the other asks for. Read both before acting on a protected path.
- A permission `allow` is not design authorization. A KiCad or library change still needs the engineer's approval of that specific change.
- Never silently alter connectivity, component values, footprints, net names, or geometry.

## Git

- Every Git mutation needs explicit, action-specific approval in chat, even where `settings.json` lets the command run without a prompt.
- Never merge a PR, force-push or `reset --hard`.
- Follow the repository's branch policy, and open PRs with `.github/pull_request_template.md`. The Git safety baseline is the global `~/.claude/rules/git-workflow.md`; `.claude/rules/git-workflow.md` adds hardware notes on top.

## External-model providers

`agent-coworker` (`agy` or `codex`) is used only when the user asks. Send it no PDFs, native KiCad files, `library/` contents, secrets, or anything on the deny or ask lists. Hooks and `settings.json` do not apply inside a provider.

## Project Instructions

- `.claude/rules/` owns the rules: `engineering.md` (design authority, change proposals, evidence labels, datasheet sources), `hardware-workflow.md` (phases, Markdown docs), `pdf.md` (project reports may be read and generated; schematic, PCB and datasheet PDFs are not read directly), `notebooklm.md` (NotebookLM procedure, path-scoped) and `git-workflow.md` (hardware Git notes).
- Respect existing project conventions, documentation, and workflows.
- Use available tools and capabilities appropriate to the task.
- Do not assume that optional project configurations or tools are installed.
- Language: follow the project's convention. If none is stated, write files and commit messages in English and reply in the user's language.

## Working Approach

1. Establish the task objective, relevant constraints, and scope from the available context.
2. Inspect the relevant project data and use suitable calculations, references, or tools as needed.
3. Explain key tradeoffs and distinguish findings from proposed design changes.
4. Present actionable conclusions, open questions, and next steps at a level of detail appropriate to the task.

## Workflow

- **Library part:** `kicad-part-start`, then `kicad-link-audit` before the part is placed. Link fixes go through `/kicad-symbol-sync` or `/kicad-footprint-sync`, with approval. The `kicad-*` skills are global (see README, Libraries); if one is not installed, say so.
- **Design data:** `sch-inspect` and `pcb-inspect` extract evidence from the saved files; `sch-review` and `pcb-review` judge it. Query narrow targets (sheet, ref, net), and brief subagents the same way with exact paths. Unannotated refs such as `U?` return every match.
- **Docs after design work:** the human runs `/progress-update`. `README.md` and `CHANGELOG.md` are maintained with `hw-git-readme` and `hw-git-changelog`.
- **Datasheets:** NotebookLM by default, one notebook per part (`notebooklm list --json`).
- **Supplier data:** JLCPCB stock and price are JavaScript-rendered and Mouser often times out, so values from search snippets stay `NOT_VERIFIED`. Spot-check key values before writing them into a design record.

## Compact Instructions

When compacting, keep: requirement, decision and open-item IDs in play, files changed and not yet committed, pending approvals and the exact change each covers, evidence labels on open values, the branch and unpushed commits, and decisions the user made this session. Do not carry over the phase; read it from `README.md` again.

## Language Rules
- Use English for all files, code, error messages, and git's activity messages.
- Use English for user-facing explanations, conversational text in CLI, unless otherwise specified by the user.
