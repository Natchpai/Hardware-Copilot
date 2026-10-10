# Hardware-Copilot

Hardware-Copilot is an independent, read-only engineering assistant for KiCad 10 projects used through Claude Code. It helps engineers inspect native schematic and PCB data, check component evidence, reason about Git changes, and record approved engineering session notes. It does not replace KiCad, a formal ERC/DRC review, a datasheet review, or human engineering authority.

Human engineers retain final authority over design decisions, review states, corrections, and releases. The repository's CAD source files remain the source of truth. The assistant proposes or reports findings; it does not silently edit design files.

## Current status

`sch-inspect v1.0` is **Stable (Scoped)**. This means the tested read-only schematic inspection path is usable for its documented evidence scope. It does not mean complete KiCad electrical-netlist parity or full-project design verification.

The repository is intended to remain small and file-based. There are no installers, automatic setup scripts, migration tools, or generated release manifests.

## Repository layout

```text
Hardware-Copilot/
├── .claude/
│   ├── rules/                 Shared engineering and Git rules
│   └── skills/                Claude Code skills
├── .github/
│   ├── pull_request_template.md
│   └── workflows/             Existing test workflow
├── hardware/                  Local KiCad test projects; gitignored
├── CLAUDE.md                  Concise repository operating guidance
└── README.md                  This document
```

The `hardware/` directory is reserved for local KiCad test projects and is ignored by Git. Do not use it as a required runtime dependency for synthetic regression tests.

## Skills

The five existing skills are Claude Code instruction packages. Their status below describes the implementation present in this repository; a skill must not claim a parser or external integration that is not actually available.

| Skill | Current implementation status |
|---|---|
| `component-check` | Available as a read-only, evidence-based component and datasheet checking workflow. It covers identity, ratings, pinout, footprint, BOM, and substitutions, but has no dedicated component parser or automatic datasheet database. |
| `git-workflow` | Available as a guarded Git/GitHub workflow for status, diff review, Conventional Commits, branch/PR preparation, and approval-aware writes. It does not authorize automatic commits, pushes, merges, or destructive history operations. |
| `pcb-inspect` | Available as a read-only KiCad PCB inspection workflow for targeted components, nets, areas, and supported checks. No dedicated PCB parser, IPC connection, or local DRC runner is bundled; unsupported evidence is reported as `NOT_VERIFIED`. |
| `sch-inspect` | Available as `v1.0 Stable (Scoped)` with the tested `query_sch.py` reader, synthetic regressions, and opt-in project-specific golden tests. Its commands and evidence boundaries are documented below. |
| `session-log` | Available only through explicit `/session-log` invocation. It prepares a concise entry and requires explicit approval before creating or appending `ENGINEERING_LOG.md`; it never runs automatically. |

Read the relevant skill document before using a skill. Shared policy is in `.claude/rules/`; the skill documents are the detailed source for scope, evidence, safety, and output rules.

## `sch-inspect v1.0` CLI

The local reader is:

```text
.claude/skills/sch-inspect/scripts/query_sch.py
```

Run it with an available Python 3 interpreter and an explicit root schematic:

```text
python .claude/skills/sch-inspect/scripts/query_sch.py <command> [target] --project <root.kicad_sch>
```

It provides nine commands:

| Command | Purpose |
|---|---|
| `summary` | Summarize discovered schematic sheets and component counts. |
| `component <ref>` | Locate a component and report its properties. |
| `sheet <name>` | Locate a hierarchical sheet by name or file. |
| `pins <ref>` | Inspect pins and local wire/label geometry. |
| `local-net <ref>` | Trace sheet-local wires, labels, junctions, and power symbols. |
| `hier-net <ref>` | Trace supported parent/child hierarchical interfaces. |
| `connected-pins <ref>` | Discover supported connected component and sheet pins. |
| `instances` | Inspect hierarchical sheet instances and reused sheet files. |
| `project-net <ref> --pin <number>` | Produce conservative project-level connectivity evidence. |

Successful commands return bounded JSON. Results can be truncated, and the response exposes missing sheets, warnings, limitations, and verification state. Invalid input, unreadable files, traversal failures, ambiguous targets, unsupported geometry, or incomplete evidence must not be converted into a positive engineering claim.

### Explicit `NOT_VERIFIED` limitations

- `project-net` is connectivity evidence, not verified KiCad netlist parity; its `project_net_verified` field remains false.
- Local geometry and matching labels do not establish complete electrical correctness.
- Complex symbol inheritance, buses, hidden connectivity, ambiguous multi-unit instances, and unsupported transforms may remain unresolved.
- Global labels and power symbols are followed only where the reader supports their semantics; repeated local labels are not automatically global.
- A truncated, empty, ambiguous, or unresolved result is not proof that a connection is absent.
- ERC is a separate optional verification activity. ERC success does not establish circuit intent or overall correctness.
- Parser errors emit `verification: NOT_VERIFIED`; the assistant must report the limitation instead of guessing.

## Tests and CI

Tests are split so synthetic coverage does not depend on a real KiCad project.

### Synthetic regression tests

The synthetic suite creates temporary `.kicad_sch` fixtures and tests the reader without `hardware/` or an external project. It includes structural, hierarchy, power-symbol, PWR_FLAG isolation, bus false-merge prevention, malformed-input, and truncation regressions.

```text
python .claude/skills/sch-inspect/tests/run_tests.py --pattern test_query_sch.py --label synthetic
```

### Project-specific golden tests

Golden tests are opt-in and use the environment variable `KICAD_GOLDEN_PROJECT` to identify an explicit root `.kicad_sch` file. The tests are read-only and hash discovered schematic files before and after execution.

- Variable absent or empty: tests report `SKIP`, not `PASS`.
- Variable configured but missing, invalid, or not a schematic file: tests report `FAIL`.
- Variable configured with a valid project: project-specific assertions run, including U103 pin 8 to R506 pin 1 connectivity and power-net isolation.

```text
python .claude/skills/sch-inspect/tests/run_tests.py --pattern test_query_sch_golden.py --label golden
```

The existing GitHub Actions workflow runs synthetic and golden suites as independent jobs and prints separate `PASS`, `FAIL`, `SKIP`, and `NOT_VERIFIED` counts.

## Manual-copy deployment

Deployment is intentionally manual. Copy the required repository files into the target project and run Claude Code from that project root. Preserve the relative `.claude/` layout and include `CLAUDE.md` when using the repository guidance. Copy `.github/` only when the target repository also wants the supplied pull-request template and workflow.

There is no installer, automatic setup, migration utility, or legacy-project conversion path. A target project must provide its own KiCad files and any required external evidence. Keep local test projects under the ignored `hardware/` directory when they are needed for manual validation.

## Portability

The repository uses relative paths, native KiCad files, Python standard-library tooling, and shell-free test fixtures so the documented workflow can be used on Windows and macOS. Windows execution has been validated in this checkout. A macOS runtime has not been validated here; macOS users should verify their available Python 3 command and local Claude Code environment before relying on a run.

## Boundaries

- Do not modify `.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, library, or other design files through this assistant.
- Do not infer PASS from counts, absent findings, or a successful parser invocation alone.
- Keep evidence scope, assumptions, unresolved items, and human follow-up explicit.
- Consult `CLAUDE.md`, `.claude/rules/`, and the relevant skill documentation for operating details.
