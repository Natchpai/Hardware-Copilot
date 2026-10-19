# Hardware-Copilot

Claude Code skills for hardware engineering with **KiCad 10**. They help with requirements, circuit design, calculations, part selection, schematic and PCB checks, debugging, and project docs.

**Hardware-Copilot helps you make engineering decisions. It does not approve designs, and it does not replace you, KiCad ERC/DRC, datasheets, simulation, or testing on real hardware.**

## What's new in v3.0.0

- **Breaking:** `hw-link-audit`, `hw-symbol-sync` and `hw-footprint-sync` are removed from this repo. Use the global `kicad-link-audit`, `kicad-symbol-sync` and `kicad-footprint-sync` skills from [kicad-workspace](https://github.com/Natchpai/kicad-workspace/tree/main/skills-src) instead (see [Libraries](#5-libraries)). If you copied the `hw-*` versions into a project, delete them and install the global ones.
- You can install the skills as a Claude Code plugin (see [Install](#install)).
- New `progress-update` skill. It updates the spec, checklist, design records, README and CHANGELOG from saved CAD data, Git history and decisions made in the session.
- New `global-rules/git-workflow.md`. It is the Git safety baseline that `.claude/rules/git-workflow.md` builds on. Install it once per user.
- `.claude/settings.json` no longer asks before edits to symbol, footprint, `library/` and STEP files. Edits to schematic, PCB and `.kicad_pro` files ask first (`.kicad_pro` was blocked before). `git push` and `gh pr create` now ask first. The `protect.json` guard did not change and still asks for all of them.
- Added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and Requirements, Contributing and License sections.

## Skills

Skills are split by **task**, not by chip, vendor or circuit type. Claude picks the skills a request needs. It does not load all of them every time.

Each skill works on its own when copied alone. It carries a short set of base rules (evidence labels, no PDF reading, KiCad files are read-only) and follows `.claude/rules/` when a project has them. If a skill mentions another skill that is not installed, it does that step itself or marks it `NOT_VERIFIED`.

The groups below follow the design stages. They are only for this README; every skill lives in `.claude/skills/<name>/`, except the global library skills in group 5.

Status: **Stable** = fixed scope with regression tests · **Used** = run on a real project, results checked · **Tested** = tried on test cases only · **Untested** = no test record yet.

### 1. Requirements and planning

| Skill | What it does | Status |
| --- | --- | --- |
| `hardware-specification` | Collects and writes hardware and PCB requirements from a beginner or engineering template | Used |
| `hardware-checklist` | Turns requirements into tasks with an owner, a status and the evidence needed | Used |

### 2. Design and parts

| Skill | What it does | Status |
| --- | --- | --- |
| `design-assist` | Requirements, circuit architecture, options and trade-offs | Tested |
| `eng-calc` | Calculations, assumptions, margins and worst-case checks | Tested |
| `component-select` | Finds and compares parts by how well they fit the circuit | Used |
| `component-check` | Checks MPN, datasheet, symbol, package, footprint and pin mapping; exact suffix and compliance may stay unverified | Tested |
| `part-spec-table` | Markdown table of part specs, one column per part number | Used |
| `stock-select` | Checks stock at DigiKey, Mouser, LCSC and the JLCPCB Parts Library | Used |
| `price-compare-table` | Markdown table of price, stock and lead time at DigiKey, Mouser, LCSC and JLCPCB | Used |

### 3. Schematic

| Skill | What it does | Status |
| --- | --- | --- |
| `sch-inspect` | Small, read-only queries of saved KiCad schematics | **Stable** |
| `sch-review` | Schematic risk review based on evidence | Used |

### 4. PCB

| Skill | What it does | Status |
| --- | --- | --- |
| `pcb-inspect` | Small, read-only queries of saved KiCad boards | **Stable** |
| `pcb-review` | PCB layout risk review based on evidence | Used |

### 5. Libraries

These are global skills. They run from `~/.claude/skills/` in every project. Their source and install steps are in [kicad-workspace `skills-src/`](https://github.com/Natchpai/kicad-workspace/tree/main/skills-src). This repo keeps no copy, so there is only one place to maintain them.

| Skill | What it does | Status |
| --- | --- | --- |
| `kicad-link-audit` | Read-only check of symbol, footprint, 3D model and library-table links | Used |
| `kicad-symbol-sync` | Splits `.kicad_sym` into `.kicad_symdir`, aligns `sym-lib-table`, fixes symbol footprint links and filters; **edits protected files only with approval**; run by name only | Used |
| `kicad-footprint-sync` | Aligns footprint libraries, local 3D paths and `fp-lib-table`; **edits protected files only with approval**; run by name only | Used |
| `kicad-naming` | Suggests or checks KLC names for symbols, footprints, 3D models and library families; advice only | Used |
| `kicad-lib-organize` | Imports, publishes and renames library items to KLC in a local library tree | Used |
| `kicad-part-start` | Starting symbol, footprint and 3D model for a new MPN in a project library | Used |

### 6. Bring-up and debug

| Skill | What it does | Status |
| --- | --- | --- |
| `debug-assist` | Possible causes of a fault and the next measurements to take | Tested |

### 7. Docs and Git

| Skill | What it does | Status |
| --- | --- | --- |
| `git-workflow` | Git status, commits and PRs, each with your approval | Used |
| `hw-git-readme` | Writes or updates project Markdown from confirmed facts | Used |
| `hw-git-changelog` | Keeps a changelog from confirmed project changes | Untested |
| `hw-git-session-log` | Optional notes on engineering decisions; run by name only | Untested |
| `hw-phase-record` | Records a project phase that you declare in an existing README | Untested |
| `progress-update` | Updates the spec, checklist, design records, README and CHANGELOG from saved CAD data, Git history and session decisions; run by name only | Used |

An inspect skill **collects evidence**. A review skill **explains what the evidence means**. Inspect output alone does not mean a design is correct.

`DRAFT`, `PRELIMINARY`, `CHECK` and `RELEASE` are phases that you declare. They are not gates, they do not mean a design is approved, and they do not give permission to commit, tag or release.

## Requirements

- [Claude Code](https://code.claude.com/docs)
- Python 3.10 or later, standard library only. Tested on Python 3.14 (Windows) and in GitHub Actions (`ubuntu-latest`).
- KiCad 10 saved files (`.kicad_sch` version `20260306`, `.kicad_pcb` version `20260206`). Older file formats are not tested.
- Optional: the global library skills from [kicad-workspace](https://github.com/Natchpai/kicad-workspace/tree/main/skills-src), and [notebooklm-py](https://github.com/teng-lin/notebooklm-py) for datasheet questions.

## Install

### Option 1: Claude Code plugin (skills only)

In Claude Code, run:

```text
/plugin marketplace add Natchpai/Hardware-Copilot
/plugin install hardware-copilot@hardware-copilot
```

On Claude Code 2.1.275 or later, one line does both: `/plugin install hardware-copilot --marketplace Natchpai/Hardware-Copilot`.

Plugin skills have a name prefix, for example `/hardware-copilot:sch-inspect`. A plugin does not load rules, `CLAUDE.md` or the file guard. For those, copy the files as in option 2.

### Option 2: copy files into a KiCad project

1. Copy what you need. Each skill works alone, so take a whole group from [Skills](#skills) or single skills. `rules/` and `hooks/` are optional; they add the full rules and file protection.

   | Copy | Why |
   | --- | --- |
   | `.claude/skills/<name>/` | The skills you want, one folder each |
   | `.claude/rules/` | Full engineering and Git rules (skills follow them when present) |
   | `.claude/hooks/` (both files) and the `hooks` block of `.claude/settings.json` | File protection guard |
   | `CLAUDE.md` | General project instructions; merge it with your own |
   | `global-rules/git-workflow.md` to `~/.claude/rules/git-workflow.md` | Git safety baseline that `.claude/rules/git-workflow.md` builds on. Install once per user, not per project. It sits outside `.claude/rules/` so it does not load twice |
   | Global `kicad-*` skills from [kicad-workspace `skills-src/`](https://github.com/Natchpai/kicad-workspace/tree/main/skills-src) | Library skills in [group 5](#5-libraries). Install once per user to `~/.claude/skills/` using that folder's README |

2. Check `.claude/settings.json` (permissions) and `.claude/hooks/protect.json` (protection rules). Edit `protect.json` to change which files are blocked, asked about or allowed; no code change is needed. The guard runs on top of `settings.json`: if `protect.json` asks for a path, you still get a prompt even when `settings.json` allows it.
3. Open the project in Claude Code and ask an engineering question in normal language. You can also call a skill by name.
4. Keep schematic and PCB files under your control. Review every design change Claude proposes.

Nothing installs or updates itself, and nothing is written back to your design on its own. Inspect and review skills never change KiCad design or library files. Protected files change only through an edit you approve, for example with the global library sync skills; the guard asks each time. Every Git write needs your approval.

### Example requests

- "Compare architecture options for a 3.3 V battery-powered design before I pick an IC."
- "Find two other ADCs with suitable ratings, then check stock at Mouser and DigiKey."
- "Inspect U103 pin 8 in the saved schematic, then review possible gate-driver risks."
- "Review decoupling placement and gate routing on the saved PCB, and say what still needs DRC or a visual check."
- "Help me find the cause of startup oscillation and suggest the next safe measurement."

## Inspection commands

The inspect scripts use only the Python standard library and print JSON with a size limit. See each skill's `SKILL.md` and the script's `--help` for the **current syntax and options**.

- **Schematic:** `summary`, `component`, `sheet`, `pins`, `local-net`, `hier-net`, `connected-pins`, `instances`, `project-net`.
- **PCB:** `summary`, `footprint`, `pads`, `net`, `tracks`, `vias`, `nearby`, `pad-distance`.

Queries read the **saved** `.kicad_sch` and `.kicad_pcb` files, not unsaved edits in the KiCad editor. Shared nets, pad-center distances and track or via geometry do not prove copper is connected, clearances are met, or the board is correct. Anything unsupported or unclear is reported as `NOT_VERIFIED`, not guessed.

## Tests and CI

Run the synthetic tests from the repository root:

```sh
python -m unittest discover -s .claude/skills/sch-inspect/tests -p 'test_query_sch.py' -v
python -m unittest discover -s .claude/skills/pcb-inspect/tests -p 'test_query_pcb.py' -v
```

**Golden tests** use real KiCad designs kept outside Git under `hardware/`. They are opt-in. With no project set, they **SKIP** instead of claiming a pass. A project path that is set but wrong makes them **FAIL**. See each test module for its environment variable and command. For schematic golden tests, set `KICAD_GOLDEN_PROJECT` to the root `.kicad_sch` file.

GitHub Actions runs the checks on every push and PR. Before you treat a green run as a real-project check, look at each job and see whether the golden tests ran or skipped.

Synthetic tests were run again for v3.0.0 (Python 3.14.7, Windows). Golden tests were not.

| Suite | Last result |
| --- | --- |
| Schematic synthetic | 21/21 passed (v3.0.0) |
| PCB synthetic | 31/31 passed (v3.0.0) |
| PCB golden (real project) | 2/2 passed (earlier run) |
| Schematic golden (real project) | 5/5 passed (earlier run) |

These are **reported test results**. They do not show that the scripts match KiCad's own netlist, ERC or DRC everywhere. Running natively on macOS and OS-level read-only sandboxing have not been checked.

## Engineering limits

- Check part specs, lifecycle, price and stock against current sources you can name. Keep facts and assumptions apart.
- **Claude never reads PDF files.** Datasheet values come from you, official web pages, or the optional `notebooklm` skill from [notebooklm-py](https://github.com/teng-lin/notebooklm-py) (you add the datasheet to a NotebookLM notebook; Claude asks it questions and cites the source). Without one of these, datasheet claims stay `NOT_VERIFIED`. See `.claude/rules/engineering.md`.
- Use the smallest query or skill that answers the question. Do not send whole designs or large netlists to the model by default.
- Every conclusion is one of: **confirmed finding**, **possible risk** or **`NOT_VERIFIED`**.
- PCB: zone fill state, full copper connectivity, clearance, return paths, SI/PI and thermal behavior are outside what the inspect script checks.
- Schematic: complex bus expansion, hidden connections, inherited symbols and unclear repeated instances may stay unresolved.
- KiCad ERC/DRC results, visual checks, simulation, measurements and manufacturer data are separate evidence. None of them is assumed to pass.

See `CLAUDE.md`, `.claude/rules/` and each skill's `SKILL.md` for how Claude works here. Hardware-Copilot does not depend on any formal review or approval process.

## Repository layout

```text
Hardware-Copilot/
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest (skills only)
│   └── marketplace.json      # Lets /plugin install from this repo
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
│       └── ...other skills...
├── global-rules/
│   └── git-workflow.md       # Git safety baseline; install to ~/.claude/rules/
├── .github/
│   ├── pull_request_template.md
│   └── workflows/
└── hardware/                 # Local KiCad test projects; not in Git
```

## How this project is built

**Read-only inspection · Your approval for every change · Small context · Standard-library scripts · Manual copy or plugin install · Tests before bug fixes**

You do not need a Git tag, checksum file or build step to use this repo.

## Contributing and support

Report bugs and ask questions in [GitHub Issues](https://github.com/Natchpai/Hardware-Copilot/issues). Pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests and commit style. Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE) © 2026 Natchpai

Hardware-Copilot is an independent project. It is not affiliated with or endorsed by Anthropic or the KiCad project.
