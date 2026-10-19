# Hardware-Copilot

A modular, evidence-driven hardware engineering assistant built for **Claude Code** and **KiCad 10**. It supports design exploration, calculations, component selection, schematic and PCB inspection, engineering reviews, and troubleshooting.

**Hardware-Copilot assists engineering decisions; it does not approve designs or replace the engineer, KiCad ERC/DRC, datasheets, simulation, or physical validation.**

## v2.1.0

- Skills are self-contained: each one works when copied alone, and follows `.claude/rules/` when the project has them.
- Skills are grouped by design stage in this README. Folders, names and commands are unchanged.
- Descriptions no longer name other skills. Mentions of other skills are optional companions with a fallback.
- `.claude/settings.json` allows `Edit` and `Write` without a prompt; edits to KiCad schematic, PCB, symbol, footprint, 3D model and `library/` files still ask.

`DRAFT`, `PRELIMINARY`, `CHECK`, and `RELEASE` are human-declared project context. They are not gates, evidence of approval, or permission to commit, tag, or release.

## What it does

Skills are organized by **engineering task**, not by a fixed chip, vendor, or circuit topology. Claude chooses relevant skills as needed rather than loading all of them for every request.

Each skill is **self-contained**: it works when copied alone. It carries a short evidence baseline (evidence labels, no PDF reads, read-only KiCad files) and follows `.claude/rules/` when the project has them. Other skills it mentions are optional companions; if one is missing, the skill does the step directly or marks it `NOT_VERIFIED`.

The skills are grouped by design stage below. The groups are for documentation and copying only; all skills stay in `.claude/skills/<name>/`, except the global KiCad skills in section 5.

### 1. Requirements and planning

| Skill | Purpose | Status |
| --- | --- | --- |
| `hardware-specification` | Gather and document hardware and PCB requirements from beginner or engineering templates | Available |
| `hardware-checklist` | Turn specification requirements into gated tasks with owner, status, and evidence | Available |

### 2. Design and parts

| Skill | Purpose | Status |
| --- | --- | --- |
| `design-assist` | Requirements, circuit architecture, alternatives, and trade-offs | Initial use tested |
| `eng-calc` | Calculations, assumptions, margins, and worst-case analysis | Initial use tested |
| `component-select` | Find and compare parts by engineering fit | Initial use tested |
| `component-check` | Verify MPN, datasheet, symbol, package, footprint, and pin mapping | Initial use tested; exact suffix/compliance may remain unverified |
| `part-spec-table` | Markdown table comparing candidate part specs, one column per part number | Available |
| `stock-select` | Check sourcing via DigiKey, Mouser, LCSC, and JLCPCB Parts Library | Initial use tested |
| `price-compare-table` | Markdown table comparing price, stock, and lead time across DigiKey, Mouser, LCSC, and JLCPCB | Available |

### 3. Schematic

| Skill | Purpose | Status |
| --- | --- | --- |
| `sch-inspect` | Targeted read-only queries of saved KiCad schematics | **v1.0 Stable (Scoped)** |
| `sch-review` | Evidence-based schematic risk assessment | Initial real-project use tested |

### 4. PCB

| Skill | Purpose | Status |
| --- | --- | --- |
| `pcb-inspect` | Targeted read-only queries of saved KiCad boards | **v1.0 Stable (Scoped)** |
| `pcb-review` | Evidence-based PCB layout risk assessment | Initial real-project use tested |

### 5. Libraries

These are global KiCad skills: they run from `~/.claude/skills/` in every project, and their source is in the kicad-workspace repo under `skills-src/`, with install steps. This repo keeps no copy. The same group also has `kicad-naming` (KLC names) and `kicad-lib-organize` (import, publish and rename library items).

| Skill | Purpose | Status |
| --- | --- | --- |
| `kicad-link-audit` | Read-only check of symbol, footprint, 3D model, and library-table links | Available; used on one real project |
| `kicad-symbol-sync` | Split `.kicad_sym` into `.kicad_symdir`, align `sym-lib-table`, fix symbol footprint links and filters; **edits protected files only with approval** | Available; used on one real project |
| `kicad-footprint-sync` | Align footprint libraries, local 3D paths, and `fp-lib-table`; **edits protected files only with approval** | Available; used on one real project |

### 6. Bring-up and debug

| Skill | Purpose | Status |
| --- | --- | --- |
| `debug-assist` | Troubleshooting hypotheses and targeted measurement plans | Initial use tested |

### 7. Docs and Git

| Skill | Purpose | Status |
| --- | --- | --- |
| `git-workflow` | Git status, commit, and PR workflow under explicit approval | Available |
| `hw-git-readme` | Create or maintain project-level Markdown using confirmed information | Available |
| `hw-git-changelog` | Maintain a human-readable changelog from confirmed project changes | Available |
| `hw-git-session-log` | Optional engineering decision notes, invoked explicitly | Available |
| `hw-phase-record` | Record an explicitly human-declared project phase in an existing README | Available |
| `progress-update` | Update the spec, checklist, design records, README, and CHANGELOG from saved CAD data, git history, and session decisions, invoked explicitly | Available; full run not yet tested |

An inspection skill **extracts evidence**; a review skill **interprets evidence**. Inspection outputs alone are not a declaration that a design is correct.

## Repository layout

```text
Hardware-Copilot/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   ├── rules/
│   ├── hooks/
│   │   ├── protect_kicad_v2.py   # PreToolUse guard for native KiCad files
│   │   └── protect.json          # deny / ask / allow rules for the guard
│   └── skills/
│       ├── sch-inspect/
│       │   ├── SKILL.md
│       │   ├── scripts/query_sch.py
│       │   └── tests/
│       ├── pcb-inspect/
│       │   ├── SKILL.md
│       │   ├── scripts/query_pcb.py
│       │   └── tests/
│       └── ...other task-oriented skills...
├── .github/
│   └── workflows/
└── hardware/               # Local KiCad test projects; gitignored
```

## Use in a KiCad project : manual copy only

1. Copy what you need into the target project. Skills are self-contained, so take a whole group from [What it does](#what-it-does) or single skills. `rules/` and `hooks/` are optional; they add the full policy and file protection:

   | Copy | Purpose |
   | --- | --- |
   | `.claude/skills/<name>/` | The skills you want, one folder each |
   | `.claude/rules/` | Full engineering and Git rules (skills follow them when present) |
   | `.claude/hooks/` (both files) + the `hooks` block of `.claude/settings.json` | File protection guard |
   | `CLAUDE.md` | General project instructions; merge with any existing one |

2. Review `.claude/settings.json` (permissions) and `.claude/hooks/protect.json` (protection rules). Adjust `protect.json` to change which files are denied, asked about, or allowed; no code change is needed. Keep the `permissions` lists in `settings.json` consistent with it.
3. Open that project in Claude Code and ask an engineering question in natural language. You can also invoke a specific skill when you want a particular workflow.
4. Keep schematic/PCB project files under human control. Review every proposed design change yourself.

There is **no installer, auto-installation, migration tool, or automatic write-back**. Inspection and review skills never modify KiCad design or library files. Protected files can change only through an explicitly approved edit, such as the library sync skills; the guard asks for approval each time. Git writes require explicit approval.

Example requests:

- “Compare architecture options for a 3.3 V battery-powered design before selecting an IC.”
- “Find two alternative ADCs with suitable ratings, then check stock at Mouser and DigiKey.”
- “Inspect U103 pin 8 in the saved schematic, then review possible gate-driver risks.”
- “Review decoupling placement and gate-routing risks on the saved PCB; state what still needs DRC or visual inspection.”
- “Help isolate the cause of startup oscillation and recommend the next safe measurement.”

## Inspection commands

The inspection parsers use Python's standard library and produce bounded JSON output. See each skill's `SKILL.md` and script `--help` for its **current CLI syntax and options**.

- **Schematic:** `summary`, `component`, `sheet`, `pins`, `local-net`, `hier-net`, `connected-pins`, `instances`, `project-net`.
- **PCB:** `summary`, `footprint`, `pads`, `net`, `tracks`, `vias`, `nearby`, `pad-distance`.

Queries reflect **saved** `.kicad_sch` / `.kicad_pcb` files, not unsaved edits in the KiCad editor. Shared net assignments, pad-center distances, and track/via geometry do not prove copper continuity, electrical clearance, or physical correctness. Unsupported and ambiguous evidence must be reported as `NOT_VERIFIED` rather than inferred.

## Tests and CI

Run synthetic regression tests from the repository root:

```sh
python -m unittest discover -s .claude/skills/sch-inspect/tests -p 'test_query_sch.py' -v
python -m unittest discover -s .claude/skills/pcb-inspect/tests -p 'test_query_pcb.py' -v
```

Project-specific **golden tests** use real KiCad designs stored outside version control under `hardware/`. They are opt-in: without a configured project, tests should clearly **SKIP**, not silently claim validation; an explicitly invalid project path should **FAIL**. Follow the corresponding test module's documented environment variable and command. For schematic golden tests, use `KICAD_GOLDEN_PROJECT` with the root `.kicad_sch` file.

GitHub Actions runs the repository's configured checks; verify the individual job results and whether any golden cases were actually executed or skipped before interpreting a green workflow as real-project validation.

Synthetic suites were re-run for v2.1.0; golden suites were not re-run.

| Suite | Last reported result |
| --- | --- |
| Schematic synthetic regression | 21/21 passed |
| PCB synthetic regression | 31/31 passed |
| PCB configured real-project golden | 2/2 passed (earlier run) |
| Real-project schematic golden | 5/5 passed in earlier validation |

These are **reported test results**, not proof of KiCad-wide netlist/ERC/DRC parity. Native macOS execution and OS-enforced sandbox read-only protection have not been independently established.

## Engineering boundaries

- Verify part specifications, lifecycle, pricing, and availability using current, attributable sources; distinguish observed facts from assumptions.
- **Claude never reads PDF documents.** Datasheet content comes from values you supply, official web pages, or the optional `notebooklm` skill (you add the datasheet to a NotebookLM notebook; Claude queries it and cites the source). Without one of these, datasheet claims stay `NOT_VERIFIED`. See `.claude/rules/engineering.md`.
- Choose the smallest relevant query or skill; avoid sending whole CAD designs or large netlists to the model by default.
- Keep conclusions traceable: **confirmed finding**, **potential risk**, or **`NOT_VERIFIED`**.
- For PCB analysis, filled-zone state, complete copper connectivity, clearance, return-path quality, SI/PI, and thermal behavior are outside the inspection parser's verified scope.
- For schematic analysis, complex bus expansion, hidden connections, inherited symbols, and ambiguous repeated instances may remain unresolved.
- Existing KiCad ERC/DRC results, visual inspection, simulations, measurements, and manufacturer data are separate evidence sources, not implied passes.

See `CLAUDE.md`, `.claude/rules/`, and each skill's `SKILL.md` for operating guidance. Hardware-Copilot is independent of any formal hardware review gate or approval framework.

## Development principles

**Read-only inspection · Explicit human approval · Minimal context · Portable standard-library queries · Manual deployment · Tests before confirmed bug fixes**

No Git tag, checksum/SHA manifest, installer, or generated release artifact is required to use this repository.
