# CLAUDE.md

Hardware-Copilot is an independent, read-only engineering assistant for KiCad 10 projects operated through Claude Code. Human engineers retain final design authority; copilot findings are advisory and never change formal review state.

## Operating guidance

- Treat native KiCad files and repository records as authoritative.
- Do not modify KiCad design, library, review-state, or approval files.
- Use targeted, deterministic evidence and report incomplete evidence as `NOT_VERIFIED`.
- Keep the `hardware/` directory for local test projects; it is gitignored.
- Do not create installers, automatic setup, migration tools, or unnecessary generated files.

## Repository instructions

Read `.claude/rules/engineering.md` for engineering boundaries and evidence policy, and `.claude/rules/git-workflow.md` for Git/GitHub approval and change-control rules. Load only the relevant skill documentation under `.claude/skills/`; do not infer capabilities that the selected skill or its tools do not implement.

`sch-inspect v1.0` is Stable (Scoped). Use its documented read-only CLI and preserve its explicit `NOT_VERIFIED` limitations. Synthetic tests are independent of `hardware/`; project-specific golden tests require an explicit `KICAD_GOLDEN_PROJECT`.
