# Hardware-Copilot

A modular, evidence-driven hardware engineering assistant built for **Claude Code** and **KiCad 10**. It supports design exploration, calculations, component selection, schematic and PCB inspection, engineering reviews, and troubleshooting.

**Hardware-Copilot assists engineering decisions; it does not approve designs or replace the engineer, KiCad ERC/DRC, datasheets, simulation, or physical validation.**

## What it does

Skills are organized by **engineering task**, not by a fixed chip, vendor, or circuit topology. Claude chooses relevant skills as needed rather than loading all of them for every request.

| Skill | Purpose | Status |
| --- | --- | --- |
| `design-assist` | Requirements, circuit architecture, alternatives, and trade-offs | Initial use tested |
| `eng-calc` | Calculations, assumptions, margins, and worst-case analysis | Initial use tested |
| `component-select` | Find and compare parts by engineering fit | Initial use tested |
| `stock-select` | Check sourcing via DigiKey, Mouser, LCSC, and JLCPCB Parts Library | Initial use tested |
| `component-check` | Verify MPN, datasheet, symbol, package, footprint, and pin mapping | Initial use tested; exact suffix/compliance may remain unverified |
| `sch-inspect` | Targeted read-only queries of saved KiCad schematics | **v1.0 Stable (Scoped)** |
| `pcb-inspect` | Targeted read-only queries of saved KiCad boards | **v1.0 Stable (Scoped)** |
| `sch-review` | Evidence-based schematic risk assessment | Initial real-project use tested |
| `pcb-review` | Evidence-based PCB layout risk assessment | Initial real-project use tested |
| `debug-assist` | Troubleshooting hypotheses and targeted measurement plans | Initial use tested |
| `git-workflow` | Git status, commit, and PR workflow under explicit approval | Available |
| `session-log` | Optional engineering decision notes, invoked explicitly | Available |

An inspection skill **extracts evidence**; a review skill **interprets evidence**. Inspection outputs alone are not a declaration that a design is correct.

## Repository layout

```text
Hardware-Copilot/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   ├── rules/
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

## Use in a KiCad project — manual copy only

1. Copy the desired `.claude/skills/` folders into the target project's `.claude/skills/` directory. Copy applicable `.claude/rules/` and review the permissions before use.
2. Open that project in Claude Code and ask an engineering question in natural language. You can also invoke a specific skill when you want a particular workflow.
3. Keep schematic/PCB project files under human control. Review every proposed design change yourself.

There is **no installer, auto-installation, migration tool, or automatic write-back**. No tool should modify KiCad design or library files as part of inspection or review. Git writes require explicit approval.

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

Reported validation at the current scoped baselines:

| Suite | Last reported result |
| --- | --- |
| Schematic synthetic regression | 21/21 passed |
| PCB synthetic regression | 31/31 passed |
| PCB configured real-project golden | 2/2 passed |
| Real-project schematic golden | 5/5 passed in earlier validation |

These are **reported test results**, not proof of KiCad-wide netlist/ERC/DRC parity. Native macOS execution and OS-enforced sandbox read-only protection have not been independently established.

## Engineering boundaries

- Verify part specifications, lifecycle, pricing, and availability using current, attributable sources; distinguish observed facts from assumptions.
- Choose the smallest relevant query or skill; avoid sending whole CAD designs or large netlists to the model by default.
- Keep conclusions traceable: **confirmed finding**, **potential risk**, or **`NOT_VERIFIED`**.
- For PCB analysis, filled-zone state, complete copper connectivity, clearance, return-path quality, SI/PI, and thermal behavior are outside the inspection parser's verified scope.
- For schematic analysis, complex bus expansion, hidden connections, inherited symbols, and ambiguous repeated instances may remain unresolved.
- Existing KiCad ERC/DRC results, visual inspection, simulations, measurements, and manufacturer data are separate evidence sources—not implied passes.

See `CLAUDE.md`, `.claude/rules/`, and each skill's `SKILL.md` for operating guidance. Hardware-Copilot is independent of any formal hardware review gate or approval framework.

## Development principles

**Read-only inspection · Explicit human approval · Minimal context · Portable standard-library queries · Manual deployment · Tests before confirmed bug fixes**

No Git tag, checksum/SHA manifest, installer, or generated release artifact is required to use this repository.
