# Hardware-Copilot

Claude Code skills for hardware engineering with **KiCad 10**. They help with requirements, circuit design, calculations, part selection, schematic and PCB checks, debugging, and project docs.

**Hardware-Copilot helps you make engineering decisions. It does not approve designs, and it does not replace you, KiCad ERC/DRC, datasheets, simulation, or testing on real hardware.**

## What's new in v4.1.0

The guard in `.claude/hooks/` now covers PDF reads and Git commands as well as KiCad file edits. Each project sets its levels in `protect.json`.

- **Git guard.** `protect_kicad_v2.py` reads git and gh commands with flags in any order, and follows `cd`, `git -C`, env prefixes and `bash -c`. The `git` block of `protect.json` names the checks:
  - deny: a push to `main` or `master` (also `HEAD:main`, `+main`, `--all`, and a bare `git push` while on `main`), `--force`, `-f` or a `+refspec`, `reset --hard`, `clean -f`, `gh pr merge`;
  - ask: `--force-with-lease`, `push --delete` or `:branch`, pushing tags, `branch -d`, `-D` or `-m`, `tag`, `gh release`, `rebase`, `commit --amend`.
  - Why: in v4.0, `git push origin --delete <branch>` ran with no prompt, because `settings.json` allows `git push *` and its deny rules match only by prefix.
- **PDF rule per project.** The `pdf` block has deny, ask and allow globs, case-insensitive, checked for the Read tool and for shell commands that name a `.pdf`. Defaults: schematic and manufacturing PDFs are denied, reports and the scratchpad are allowed, and every other PDF asks.
- **Datasheet fallback.** A datasheet PDF moves from "never" to "ask". NotebookLM stays the default. Claude reads a datasheet PDF only after you approve that file in chat, reads only the pages it needs, cites file, revision, page and table, and never uploads it.
- **Rule order** in the guard is now deny > ask > allow, like Claude Code. A denied or asked glob wins over an allowed folder: a `.kicad_sch` under `scratchpad/` now asks, and a `.wrl` under `library/` is denied.
- **`settings.json` is shorter.** The `Edit(...)` allows that the blanket `Edit` already covers, and the Git and PDF prefix rules, are gone; the guard owns them. `gh pr merge` stays denied as a second line.
- **One `workflow.md`** replaces `hardware-workflow.md` and `project-workflow.md`.
- `tools/check_permissions.py` checks the `protect.json` shape, the git check names, the PDF deny in both folder spellings, and the hook matcher (now with `Read`). `tools/tests/test_hook.py` covers the guard.

### Upgrading from v4.0

1. `python tools/sync_project.py <project root> --ref v4.1.0`, check the plan, then add `--apply`. It replaces the hook and an unedited `protect.json`, and removes the two old workflow rules.
2. Merge `settings.json` by hand from the printed diff: add `Read` to the hook matcher and drop the lines the guard now owns.
3. If you edited `protect.json`, add the `pdf` and `git` blocks from the release copy.
4. Run `python tools/check_permissions.py <project root>`.
5. In the project `CLAUDE.md`, point to `workflow.md` instead of the two old rules.

## Changes in v4.0.0

**v4.0.1:** the `progress-update` preflight ignores `.kicad_pro` files under `.claude/`. In v4.0.0, the `sch-inspect` test fixture made a synced project show two KiCad projects, so the preflight stopped unless you passed `--project`.

v4.0.0 removes and merges skills (see **Upgrading from v3**). It also adds checks so that skills, rules and project copies stay in step.

- **One table reader for the spec and checklist** (`progress-update/scripts/register.py`).
  - It reads DEC, OPEN, REF, task, gate and change-note rows by header name, then by position.
  - `register.py lint` and the preflight report `duplicate_id`, `bad_status`, `closed_no_date`, `rev_order`, `long_task` and REF revision drift.
  - A DEC that cites `OPEN-031 item 5` now matches only rows that name that item.
- **One history.** The spec change-note is the design history. `progress-update sync` writes one CHANGELOG pointer line per spec revision instead of a second copy.
- **`hw-docs`** replaces `hw-git-readme`, `hw-git-changelog` and `hw-phase-record`, with readme, changelog and phase modes.
- **`table` mode** in `stock-select` (price, stock and lead time) and in `component-select` (specs). These replace `price-compare-table` and `part-spec-table`.
- **`hardware-checklist` rule 10:** a task row holds the statement, the current state and `Left:`. History goes to the spec change-note.
- **One source for each rule.**
  - `shared/evidence-baseline.md` is copied word for word into every hardware skill.
  - `tools/check_skills.py` and `tools/check_permissions.py` catch drift, in CI and on any project.
  - New rule `.claude/rules/project-workflow.md` holds the spec, checklist and doc cycle, team messages and open checks (merged into `workflow.md` in v4.1.0).
  - The `CLAUDE.md` template has Project and Layout placeholders.
- **`sch-inspect` 1.3.0:**
  - `netlist` and `netlist-compare` check the `project-net` graph against KiCad's own netlist.
  - They run `kicad-cli` only when you ask, on a temp copy of the sheets.
  - On a real 13-sheet project: 176 nets and 838 pins, 0 differences.
- **`tools/sync_project.py`** updates a project's skills, rules and hooks from a release tag.
  - It does a dry run by default and keeps a lock file.
  - It never writes `settings.json`.

### Upgrading from v3

| Removed in v4.0.0 | Use instead |
| ------------------ | --- |
| `hw-git-readme` | `hw-docs readme` |
| `hw-git-changelog` | `hw-docs changelog` |
| `hw-phase-record` | `hw-docs phase` |
| `hw-git-session-log` | none (removed) |
| `price-compare-table` | `stock-select table` |
| `part-spec-table` | `component-select table` |

For a project that copied v3 by hand, run `python tools/sync_project.py <project root> --ref v4.0.0 --baseline <the v3 tag you copied>`. Check the plan, then add `--apply`. Files you edited are kept and listed. Merge the printed `settings.json` lines by hand.

## Changes in v3.4.0

- `progress-update` reviews open items, task status and summary lists (`review:*` findings) and asks before closing anything; `light` and `sync` modes; one spec revision per commit.
- `hardware-checklist` uses the spec's open-item table as the only register.

Earlier changes are in [Releases](https://github.com/Natchpai/Hardware-Copilot/releases).

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
| `component-select` | Finds and compares parts by how well they fit the circuit; `table` mode builds a spec table, one column per part number | Used |
| `component-check` | Checks MPN, datasheet, symbol, package, footprint and pin mapping; exact suffix and compliance may stay unverified | Tested |
| `stock-select` | Checks stock at DigiKey, Mouser, LCSC and the JLCPCB Parts Library; `table` mode builds a price, stock and lead-time table for known part numbers | Used |

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
| `hw-docs` | Creates or updates the root README and CHANGELOG from confirmed facts, and records a phase you declare | Used |
| `progress-update` | Updates the spec, checklist, design records, README and CHANGELOG from saved CAD data, Git history and session decisions, and reviews open items, task status and summary lists for stale entries; closes nothing without your answer; run by name only | Used |

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
   | `.claude/rules/` | Full engineering, workflow and Git rules (skills follow them when present); `workflow.md` holds the phases and the standard spec, checklist and doc cycle |
   | `.claude/hooks/` (both files) and the `hooks` block of `.claude/settings.json` | Guard for KiCad file edits, PDF reads and Git commands |
   | `CLAUDE.md` | Project template: fill in the Project and Layout sections; the rest points to the rules |
   | `global-rules/git-workflow.md` to `~/.claude/rules/git-workflow.md` | Git safety baseline that `.claude/rules/git-workflow.md` builds on. Install once per user, not per project. It sits outside `.claude/rules/` so it does not load twice |
   | Global `kicad-*` skills from [kicad-workspace `skills-src/`](https://github.com/Natchpai/kicad-workspace/tree/main/skills-src) | Library skills in [group 5](#5-libraries). Install once per user to `~/.claude/skills/` using that folder's README |

2. Check `.claude/settings.json` (permissions) and `.claude/hooks/protect.json` (protection rules). Edit `protect.json` to change which files are blocked, asked about or allowed, which PDFs Claude may read, and which Git commands are blocked or asked about; no code change is needed. The guard runs on top of `settings.json`: if `protect.json` asks for a path, you still get a prompt even when `settings.json` allows it.
3. Open the project in Claude Code and ask an engineering question in normal language. You can also call a skill by name.
4. Keep schematic and PCB files under your control. Review every design change Claude proposes.

Nothing installs or updates itself, and nothing is written back to your design on its own. Inspect and review skills never change KiCad design or library files. Protected files change only through an edit you approve, for example with the global library sync skills. The guard asks before every schematic and PCB edit. Every Git write needs your approval.

### Update a project

`tools/sync_project.py` copies `.claude/skills/`, `.claude/rules/` and `.claude/hooks/` from a release tag of this clone into a project. It does a dry run unless you pass `--apply`:

```text
python tools/sync_project.py <project root> --ref v4.1.0              # show the plan
python tools/sync_project.py <project root> --ref v4.1.0 --apply      # write it
```

- It keeps `.claude/hardware-copilot.lock.json` in the project with a hash of each file it wrote.
- A file you edited in the project is kept and reported, unless you name it with `--overwrite <path>`.
- Your own skills are never touched.
- Files the release dropped are removed only if you did not edit them.
- `settings.json`, `settings.local.json` and `memory/` are never written. For `settings.json` it prints the permission lines that differ, for you to merge.
- `--exclude skills/<name>` skips a path from then on.
- On the first sync of a project you copied by hand, add `--baseline <old tag>`. Files equal to that release then update cleanly.

`tools/check_permissions.py <project root>` checks that the project's `settings.json` still agrees with `protect.json`.

### Example requests

- "Compare architecture options for a 3.3 V battery-powered design before I pick an IC."
- "Find two other ADCs with suitable ratings, then check stock at Mouser and DigiKey."
- "Inspect U103 pin 8 in the saved schematic, then review possible gate-driver risks."
- "Review decoupling placement and gate routing on the saved PCB, and say what still needs DRC or a visual check."
- "Help me find the cause of startup oscillation and suggest the next safe measurement."

## Inspection commands

The inspect scripts use only the Python standard library and print JSON with a size limit. See each skill's `SKILL.md` and the script's `--help` for the **current syntax and options**.

- **Schematic:** `summary`, `components`, `component`, `sheet`, `pins`, `local-net`, `hier-net`, `connected-pins`, `instances`, `project-net`, `net`, `bus`.
- **PCB:** `summary`, `footprint`, `pads`, `nets`, `net`, `tracks`, `vias`, `zones`, `nearby`, `pad-distance`.

Queries read the **saved** `.kicad_sch` and `.kicad_pcb` files, not unsaved edits in the KiCad editor. Shared nets, pad-center distances and track or via geometry do not prove copper is connected, clearances are met, or the board is correct. Anything unsupported or unclear is reported as `NOT_VERIFIED`, not guessed.

## Tests and CI

Run the synthetic tests from the repository root:

```sh
python -m unittest discover -s .claude/skills/sch-inspect/tests -p 'test_query_sch.py' -v
python -m unittest discover -s .claude/skills/pcb-inspect/tests -p 'test_query_pcb.py' -v
python .claude/skills/progress-update/tests/test_review_items.py
python .claude/skills/progress-update/tests/test_register.py
```

The `progress-update` regression cases read the history of the project the review was built on; in any other repository they **SKIP**.

**Golden tests** use real KiCad designs kept outside Git under `hardware/`. They are opt-in. With no project set, they **SKIP** instead of claiming a pass. A project path that is set but wrong makes them **FAIL**. See each test module for its environment variable and command.

Schematic golden tests need two variables. With either one unset, they skip.

- `KICAD_GOLDEN_PROJECT`: absolute path of the project's root `.kicad_sch` file.
- `KICAD_GOLDEN_EXPECT`: absolute path of a JSON file with the expected values for that project.

```sh
KICAD_GOLDEN_PROJECT=/abs/path/Top.kicad_sch \
KICAD_GOLDEN_EXPECT=/abs/path/golden.json \
python .claude/skills/sch-inspect/tests/run_tests.py --pattern test_query_sch_golden.py --label golden
```

The JSON file holds a list of `cases`. Each case runs one `query_sch.py` command and checks its result. Start from [golden.example.json](.claude/skills/sch-inspect/tests/golden.example.json), which holds the values of one real project, and replace them with values you checked in KiCad.

| Key | Meaning |
| --- | --- |
| `name` | Label shown when the case fails. |
| `command` | Command and arguments, for example `["project-net", "U103", "--pin", "8"]`. `--project` is added by the test. |
| `status` | Expected `status` of the single result. |
| `has_pins`, `lacks_pins` | `[reference, pin]` pairs that must, or must not, be in `connected_component_pins`. |
| `has_power`, `lacks_power` | Names that must, or must not, be in `power_net_names`. |
| `has_global`, `lacks_global` | Names that must, or must not, be in `global_labels`. |
| `has_sheet_names` | Sheet names that `instances` must list. |

An unknown key fails the case. A pin or name check on a truncated result also fails, because a truncated list cannot show that an item is absent.

PCB golden tests work the same way, with their own two variables.

- `KICAD_PCB_GOLDEN_BOARD`: absolute path of the `.kicad_pcb` file.
- `KICAD_PCB_GOLDEN_EXPECT`: absolute path of a JSON file with the expected values for that board.

```sh
KICAD_PCB_GOLDEN_BOARD=/abs/path/board.kicad_pcb \
KICAD_PCB_GOLDEN_EXPECT=/abs/path/golden.json \
python .claude/skills/pcb-inspect/tests/run_tests.py --pattern test_query_pcb_golden.py --label golden
```

Each case has `name`, `command`, an optional `status`, and `fields`, a map from a field path to its expected value, for example `"pads[number=1].position"` or `"tracks[0].length_mm"`. Start from [golden.example.json](.claude/skills/pcb-inspect/tests/golden.example.json); the format is described in [testing.md](.claude/skills/pcb-inspect/references/testing.md).

GitHub Actions runs the checks on every push and PR. Before you treat a green run as a real-project check, look at each job and see whether the golden tests ran or skipped.

Synthetic tests were run again for v3.1.0 (Python 3.14.7, Windows). For v3.2.0 the schematic synthetic and golden tests were run on macOS (Python 3.15). For v3.3.0 the PCB synthetic and golden tests were run on macOS (Python 3.15). For v3.3.1 all four suites were run on macOS (Python 3.15). CI runs the schematic and PCB synthetic tests on Linux, Windows and macOS.

| Suite | Last result |
| --- | --- |
| Schematic synthetic | 38/38 passed (v3.3.1, macOS) |
| PCB synthetic | 48/48 passed (v3.3.1, macOS) |
| PCB golden (real project) | 6/6 cases passed (v3.3.1, one local project) |
| Schematic golden (real project) | 12/12 cases passed (v3.3.1, one local project) |
| `progress-update` review | 10/10 passed in the source project, 8 passed and 2 skipped here (v3.4.0, Windows, Python 3.14) |

These are **reported test results**. They do not show that the scripts match KiCad's own netlist, ERC or DRC everywhere. Running natively on macOS and OS-level read-only sandboxing have not been checked.

## Engineering limits

- Check part specs, lifecycle, price and stock against current sources you can name. Keep facts and assumptions apart.
- **Claude never reads schematic or PCB PDFs directly**, and reads a datasheet PDF only after you approve that file. It may read the project's own report PDFs and build report PDFs when you ask. Datasheet values come from the optional `notebooklm` skill from [notebooklm-py](https://github.com/teng-lin/notebooklm-py) by default (the datasheet sits in a NotebookLM notebook; Claude asks it questions and cites the source), or from you or official web pages. Claude asks before uploading a PDF, and asks you what to do if NotebookLM has a problem. A direct read of a datasheet cites file, revision, page and table. Without a source, datasheet claims stay `NOT_VERIFIED`. See `.claude/rules/pdf.md`.
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
│   │   ├── protect_kicad_v2.py   # PreToolUse guard: KiCad edits, PDF reads, Git commands
│   │   └── protect.json          # deny / ask / allow rules, pdf and git blocks
│   └── skills/
│       ├── sch-inspect/
│       │   ├── SKILL.md
│       │   ├── scripts/query_sch.py
│       │   └── tests/
│       ├── pcb-inspect/
│       │   ├── SKILL.md
│       │   ├── scripts/query_pcb.py
│       │   └── tests/
│       ├── progress-update/
│       │   ├── SKILL.md
│       │   ├── scripts/progress_preflight.py
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
