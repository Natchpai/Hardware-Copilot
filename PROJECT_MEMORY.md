# Hardware-Copilot — Project Memory & Roadmap

> **Local continuity document** | Updated: 2026-10-11 | Status: **v1.1.0 candidate — pre-PR validation complete; PR/CI pending**.
>
> Purpose: carry architecture decisions, implemented scope, acceptance evidence, constraints, and future work into subsequent Claude Code/Codex sessions. This is a **human-readable memory file**, not an authoritative live repository inventory or a new review-state system.

## 1. Vision and success criteria

**Hardware-Copilot** is an independent, multi-purpose AI assistant for hardware engineering in **Claude Code**, working with **KiCad 10** projects. It should help engineers:

- reason about design requirements, architectures, topology choices, trade-offs, and constraints;
- perform engineering calculations, worst-case assessments, and sanity checks;
- discover and compare interchangeable components and current distributor/assembly stock;
- inspect saved native KiCad schematic/PCB structures through targeted, read-only tools;
- review schematic and PCB risks using evidence, datasheets, calculations, and targeted human inspection;
- troubleshoot symptoms, plan discriminating measurements, and document decisions;
- use Git/GitHub workflows with explicit human approval for state-changing actions.

**Key principle:** *Skills define how to work, not what to design.* Do not hardcode device families, MPNs, manufacturers, or circuit topologies into general engineering Skills. Claude may research relevant current datasheets, application notes, manufacturers and distributors when needed. Prefer a small evidence-backed shortlist and a clear stopping criterion over endless part searches.

Human engineers retain final design and approval authority. The copilot provides engineering assistance and findings, not certification. It is **separate from the Hardware Review Framework** and has no mandatory gates, migrated state, or formal review workflow.

## 2. Non-negotiable implementation decisions

1. **Read-only CAD:** Do not modify KiCad `.kicad_sch`, `.kicad_pcb`, libraries, project configuration, review/approval records, or hardware settings. Native saved CAD files are the data authority within their supported inspection scope.
2. **Minimal context:** Use on-demand Skills, targeted native-file queries and bounded JSON outputs; avoid loading entire CAD files, PDFs/images or huge netlists into the model context by default.
3. **Prefer native file queries:** Parser tools use portable Python standard library; no obligatory KiCad GUI, automatic export or external Python packages for routine queries.
4. **Honest evidence boundaries:** Distinguish confirmed evidence, potential risks, assumptions, and `NOT_VERIFIED`. Neither net names nor geometry alone establish electrical connectivity or design correctness.
5. **Manual deployment only:** Copy the relevant `.claude/` files into an existing KiCad project manually when desired. **No auto-installer, auto-migration or automatic project setup.**
6. **No SHA/Checksum artifacts:** Do not generate SHA files, checksum manifests, freeze archives or extra state files. Test code may use in-memory hashes to verify read-only behavior.
7. **No mandatory Git tag:** Git tags are not needed for current release management. Do not create tags without an explicit new request.
8. **Git actions need approval:** Do not commit, push, open PRs or modify release state without explicit authorization. Existing code convention: Conventional Commits (`feat:`, `fix:`, etc.), branches `feat/`, `fix/`, `docs/`, `chore/`.
9. **Work incrementally:** Keep each Skill concise, reuse tools and other Skills rather than duplicating parsers, and avoid speculative feature expansion.
10. **Cross-platform:** Target Windows and macOS via `pathlib` and portable Python; **macOS native execution was not independently confirmed** in reported SCH acceptance tests.

## 3. Repository and deployment layout

Repository: **`Hardware-Copilot`**, private GitHub repository. The user reported initial push on `origin/main`, initial commit `9d6b02f` (`feat: initialize hardware copilot with schematic inspection`), and later committed all project documentation. **Current exact HEAD SHA and final CI run after the latest commits are not supplied here.** Do not treat the initial SHA as current HEAD.

Illustrative active layout (verify against repository before editing):

```text
Hardware-Copilot/
├── CLAUDE.md
├── README.md
├── .gitignore
├── .github/
│   ├── workflows/
│   └── pull_request_template.md
├── .claude/
│   ├── settings.json
│   ├── rules/
│   │   ├── engineering.md
│   │   └── git-workflow.md
│   ├── hooks/
│   └── skills/
│       ├── design-assist/SKILL.md
│       ├── eng-calc/SKILL.md
│       ├── component-select/SKILL.md
│       ├── stock-select/SKILL.md
│       ├── component-check/SKILL.md
│       ├── sch-inspect/
│       │   ├── SKILL.md
│       │   ├── references/schematic-data.md
│       │   ├── scripts/query_sch.py
│       │   └── tests/{test_query_sch.py,test_query_sch_golden.py}
│       ├── pcb-inspect/
│       │   ├── SKILL.md
│       │   ├── scripts/query_pcb.py
│       │   └── tests/{test_query_pcb.py,test_query_pcb_golden.py}
│       ├── sch-review/SKILL.md
│       ├── pcb-review/SKILL.md
│       ├── debug-assist/SKILL.md
│       ├── git-workflow/SKILL.md
│       └── session-log/SKILL.md
└── hardware/                  # Local real KiCad projects; gitignored
    └── 2Phase_SynchBuck/      # Real-project validation example
```

`/hardware/` is deliberately excluded from Git; `__pycache__/` is ignored. Test/deployment files under `.claude/` can be committed, but local design data must not be committed accidentally. The user wanted manual copy between repositories, not an installer or update mechanism.

## 4. Capability architecture

**One primary Claude Code assistant + task-oriented Skills + deterministic inspection utilities**. No default “one agent per skill” requirement.

| Skill | Responsibility | Reported status |
|---|---|---|
| `design-assist` | General design reasoning, requirements, candidate architectures and trade-offs; no fixed IC/topology | Informal real-use test passed |
| `eng-calc` | Equations, units, nominal/worst case, tolerance, derivations and checked assumptions; no fixed calculator library | Informal test passed |
| `component-select` | Engineering suitability, shortlist 2–3 candidates, hard constraints, life-cycle and datasheet trade-offs | Informal test passed |
| `stock-select` | Distributor/assembly sourcing at DigiKey, Mouser, LCSC and JLCPCB parts library; price/MOQ/stock/availability evidence | Informal test passed |
| `component-check` | Exact MPN, datasheet ratings, pinout, symbol–footprint mapping, package and BOM consistency | Real-project scoped test passed; details pending |
| `sch-inspect` | Saved KiCad schematic structural/connectivity **evidence** via `query_sch.py` | **v1.0 Stable (Scoped)** |
| `pcb-inspect` | Saved KiCad PCB geometry, assignments and routing **evidence** via `query_pcb.py` | **v1.0 Stable (Scoped)** |
| `sch-review` | Risk-oriented electrical schematic review, combining schematic evidence, calculations, datasheets as needed | Informal real-project test passed |
| `pcb-review` | PCB layout engineering review of placement, routing, returns, thermal/manufacturing risk using bounded evidence | Informal real-project test passed |
| `debug-assist` | Lightweight symptoms → hypotheses → targeted safe measurements → revision of diagnosis; **SKILL.md only, no Python** | Informal test passed |
| `git-workflow` | Git status/commit/PR guidance with human approval | Skill exists |
| `project-readme` | Explicit project README creation or narrow update from confirmed information | v1.1.0 candidate |
| `phase-record` | Explicit human-declared phase acknowledgement or in-place README phase update | v1.1.0 candidate |
| `project-changelog` | Explicit, human-curated CHANGELOG maintenance | v1.1.0 candidate |
| `session-log` | Optional, manual decision capture to `ENGINEERING_LOG.md`, only with approval | Skill exists |

**Inspection is distinct from review.** Inspection retrieves structural facts; review combines evidence with engineering judgment and assigns confirmed defects, possible risks and `NOT_VERIFIED`. No automatic change of design/review state.

### Skill orchestration examples

- “Help design a power supply” → `design-assist`, then `eng-calc`, optionally `component-select`/`stock-select`.
- “Find alternatives to part X that are in assembly stock” → `component-select` (functional fitness), then `stock-select` (supplier-specific evidence), then `component-check` as needed.
- “What is connected to U103 pin 8?” → `sch-inspect` only if structural lookup suffices.
- “Review gate-drive circuitry” → `sch-review` using `sch-inspect`, then calculations/part evidence only when relevant.
- “Review power-loop placement” → `pcb-review` using `pcb-inspect`, schematic intent as necessary, and external KiCad DRC/visual evidence if provided.
- “Buck converter oscillates after startup” → `debug-assist` with targeted diagnostic steps; do not infer a root cause from symptoms alone.

## 5. Schematic inspection: frozen functional scope

`sch-inspect v1.0 — Stable (Scoped)` offers **nine CLI commands**:

| Command | Intent |
|---|---|
| `summary` | Discover project hierarchy and schematic counts |
| `component <ref>` | Locate reference and inspect properties |
| `sheet <name>` | Locate named hierarchical sheet |
| `pins <ref>` | Resolve symbol pins and local geometric evidence |
| `local-net <ref>` | Sheet-local wires, junctions, labels and supported power markers |
| `hier-net <ref>` | Targeted hierarchical parent–child interface evidence |
| `connected-pins <ref>` | Connected component/sheet-pin evidence in supported traversal |
| `instances` | Enumerate sheet instances/reused files |
| `project-net <ref> --pin <num>` | Project-level graph evidence including supported labels/power/hierarchy |

Important regressions and fixes:

- Hierarchical tracing from **U103 pin 8** to **R506 pin 1**, through Power State and MCU IOs; naming changes between sheet interfaces can be intentional.
- **`PWR_FLAG` is an ERC driver marker, NOT a globally shared net name.** Erroneous union previously merged `+9V` and GND; fixed and negatively tested.
- Labels on **bus geometry must not be merged into scalar-net groups**.
- Malformed geometry and ambiguous/unsupported semantics must return structured `NOT_VERIFIED`/error, never fake connectivity or uncaught traceback.

Reported validation trajectory: regression 14 → 20 → **21/21** pass; real-project schematic golden **5/5** pass. KiCad 10.0.6 native S-expression netlist was generated **temporarily for targeted validation**, with an existing annotation warning; temp netlist and isolated config were removed. This was a one-time validation technique, **not the normal query workflow**.

**Still not verified:** KiCad full-netlist/ERC parity, bus expansion/entries, inherited-symbol resolution, hidden connectivity, difficult repeated/ambiguous instances, and native macOS runtime; access-control sandbox enforcement is separate from a read-only script.

## 6. PCB inspection: frozen functional scope

`pcb-inspect v1.0 — Stable (Scoped)` offers exactly **eight commands** (do not expand without a deliberate scope decision):

| Command | Intent / metric |
|---|---|
| `summary` | Board/layer/footprint overview |
| `footprint <ref>` | Footprint ID, value, saved origin/rotation/layer |
| `pads <ref>` | Pad type, shape, size, layers, net assignment, transformed board-space center |
| `net <name>` | Saved pad net **assignments**; not conductive-path evidence |
| `tracks <net>` | Saved track segment/arc primitives: width, endpoints, layer, geometry/length when resolvable |
| `vias <net>` | Via geometry, drill/size, type, span and assigned net |
| `nearby <ref>` | Nearby footprints by Euclidean distance between **footprint origins** |
| `pad-distance <ref.pin> <ref.pin>` | Euclidean center-to-center distance between **pad centers**, not copper clearance |

Engineering guardrails:

- Board-space coordinates in millimeters; account for rotation and backside/mirroring. Handle unusual identifiers and duplicate pads/references as ambiguity rather than arbitrary selection.
- Preserve `MISSING`, `UNCONNECTED`, `ASSIGNED_WITHOUT_DECLARATION`, `AMBIGUOUS`, malformed geometry `NOT_VERIFIED`, and bounded/truncated output semantics as appropriate.
- Same net name does **not** prove copper is physically connected. Center distance is **not** copper clearance. Track counts are **not** signal-path length or routing completeness.
- Parser deliberately omits filled-zone connectivity, actual copper-path graph, clearance/DRC parity, physical shorts/opens, stackup effects, signal/thermal simulations and electrical intent.

Reported validation progression: v0.1 synthetic 7/7; v0.2 14/14; v0.3 19/19; v0.4 26/26; final hardening **31/31**. Configured real PCB golden **2/2**; unconfigured golden tests **SKIP 2**; explicitly invalid configured board must **FAIL**, not silently skip. Golden test ensures board bytes unchanged.

Real-project examples: `R313.1`–`R313.2` pad-center distance **1.65 mm**; net `/Top/Power Supplies/+5VUSB` yielded **18 track primitives and 1 via**. Native independent KiCad evidence was used for golden expectations per Codex report. `nearby R313` identified **305 neighboring footprints** in the examined board. Python 3.14 launcher produced a runtime path warning on the user's host even while queries and tests exited successfully; root cause was not confirmed.

## 7. Engineering reviews and sourcing: verified behavioral boundaries

- `sch-review`: on the real Power State/gate-driver area, found topology consistent with available evidence and no confirmed defect; flagged conditional risks for EN timing, diode pulse margin, capacitor qualification and rail transients. Lack of confirmed defects is **not** full design approval.
- `component-check`: scoped real-project test verified symbol/package/pinout consistency; exact orderable suffix, detailed electrical/package compliance remained `NOT_VERIFIED`.
- `pcb-review`: assessed gate-driver loop/decoupling geometry without alleging a short or open. Examples: HO driver-to-resistor pad-center distance 14.467 mm; LO distance 7.182 mm; routing via transitions; nearby decoupling/boot capacitors. It correctly requested manual review of return path, zone fill and KiCad DRC. Saved-board data cannot reflect unsaved editor changes.
- `component-select`: **engineering selection**, independent of seller stock; eliminate hard-constraint failures before weighing preferences; do not overproduce candidates. No fixed MPNs.
- `stock-select`: **procurement/assembly stock** from DigiKey, Mouser, LCSC and JLCPCB. **LCSC stock is not identical to JLCPCB assembly availability.** Verify supplier part ID, exact MPN, currency/price/MOQ and when the evidence was checked. Do not purchase or reserve automatically.
- `debug-assist`: symptom-driven and safety-conscious; separate observed facts from hypotheses, propose discriminating measurements with proper references and safe probe methodology; do not create debug logs or scripts unless requested.

## 8. Tests, CI and release record

### v1.1.0 pre-PR validation (2026-10-11)

This candidate adds portable Git workflow guidance, a lightweight human-declared
hardware phase vocabulary, and project README, phase-record, and changelog
Skills. These additions do not create phase gates, automatic transitions,
release-state records, PDF processing, or KiCad design writes.

Fresh local validation on the candidate branch:

| Check | Result |
|---|---|
| SCH synthetic regression | **21/21 PASS** |
| PCB synthetic regression | **31/31 PASS** |
| SCH golden without configured project | **SKIP 5** as designed |
| PCB golden without configured board | **SKIP 2** as designed |
| Rules/Skills integration audit | **PASS**: no rule-to-rule includes/links; Skills do not reference `.claude/rules/`; Git and phase approval boundaries align |
| Documentation-skill contract checks | **PASS**: human-declared phase only, no inferred default, static Mermaid workflow, no release Git action |

`v1.1.0` remains a candidate until the pull request is reviewed, merged, and
its CI results are checked. A Git tag and GitHub Release remain separate,
explicitly approved actions.

Reported results by user and Codex (do not claim these were re-run in this document's creation):

| Check | Latest reported result |
|---|---|
| Schematic synthetic regression | **21/21 PASS** |
| Schematic real-project golden | **5/5 PASS** |
| PCB synthetic regression | **31/31 PASS** |
| PCB configured real-project golden | **2/2 PASS** |
| Golden without configured project | SKIP, not fabricated PASS |
| Explicit invalid golden project | FAIL as intended |
| Read-only on real KiCad files | PASS via test hash guards |
| GitHub Actions initial successful run | **38032558295**, both synthetic and project-specific golden jobs reported success on `main` |
| Repository-level integration audit | **PASS**, as reported by user |
| Recent commits/tags | Docs and other changes reported committed; **no Git tag required**; current exact HEAD not independently established |

GitHub Actions results should always be evaluated by actual executed assertion/test counts: a SKIP-only golden job is not a verified golden run. Check current workflow logs after subsequent changes rather than assuming prior success applies to every later commit.

### GitHub Actions workflow responsibilities (`.github/workflows/`)

**Verified from reported runs, not the YAML source:** The private repository has GitHub Actions configured on `main`. Run **38032558295** was reported `success`, with separate synthetic-regression and project-specific golden-test jobs reported successful. Later local validation reported SCH synthetic **21/21**, PCB synthetic **31/31**, SCH golden **5/5**, and PCB golden **2/2**. **Do not attribute these latest counts to run 38032558295 without inspecting its logs.**

**Intended CI behavior to preserve or verify:**

| CI concern | Expected policy / check |
|---|---|
| Synthetic tests | Run self-contained Python `unittest` suites for SCH and PCB without accessing local `hardware/` |
| Golden tests | Run only with an explicitly provisioned real project; treat actual executed tests as PASS, absent configuration as SKIP, and invalid configured paths as FAIL |
| Repository permissions | Prefer read-only workflow permissions, especially for pull requests or external contributors |
| Design data | Never commit, upload as build artifacts, or expose private PCB/schematic data or secrets accidentally |
| Reports | Keep synthetic, golden, SKIP, FAIL and `NOT_VERIFIED` distinct; do not report skipped tests as validated |
| Change control | Modify workflow YAML only with approval; no automatic installer, release tags, checksum/SHA manifests or forced pushes |

**Still not established from source files:** Exact workflow YAML filenames, event triggers (`push`/`pull_request`/manual), runner operating systems, matrix, environment variables, how the golden fixtures are provisioned in CI, `permissions`, and artifact/upload settings. Read the current `.github/workflows/*.yml` / `*.yaml` directly before updating or making claims about these details. Private repository visibility alone does not establish whether actual design files are present on a CI runner.

**Recommended CI audit:** Check the workflow definition and latest run associated with the current commit, inspect individual job logs and non-skipped assertion counts, confirm secrets/fixtures are protected, then run tests with no golden fixture and with an invalid explicit golden path to confirm correct SKIP/FAIL behavior.

Example local test entry points (run from repository root):

```powershell
python -m unittest discover -s .claude/skills/sch-inspect/tests -v
python -m unittest discover -s .claude/skills/pcb-inspect/tests -v
```

The schematic golden suite uses an explicit `KICAD_GOLDEN_PROJECT` pointing to the real root `.kicad_sch`. The PCB golden suite uses a configuration documented in its current test file; **inspect that file before assuming a specific environment-variable name**. Real KiCad files live in ignored `hardware/` and should be absent from public/CI synthetic fixtures unless specifically provisioned. Preserve test independence when sharing the repo.

## 9. How to continue development safely

1. **Check reality first:** inspect current `README.md`, `CLAUDE.md`, `.claude/rules/`, `SKILL.md`, CLI `--help`, current tests and `git status` before editing; this memory is contextual, not a replacement for the working tree.
2. **Choose smallest tool/skill:** prefer targeted data, limited JSON output, and only relevant references/datasheets; do not open every skill by default.
3. **For parser issues:** reproduce on a minimal synthetic fixture; first add failing negative/positive regression coverage; make a narrow root-cause fix without breaking CLI/JSON compatibility; rerun real golden tests when available.
4. **For a review:** specify question and scope, label findings as confirmed defect, potential risk, or `NOT_VERIFIED`, give evidence/impact/next check. Never treat missing DRC or visual review as PASS.
5. **Before state changes:** seek explicit approval for KiCad changes, Git commit/push/PR or release actions; no tags/installer/checksum files by default.
6. **Respect manual deployment:** copying `.claude/` as selected is the supported workflow; don't build an installer. When copied to a different KiCad project, adjust explicit real-test paths outside skill logic and test routing/path resolution.

## 10. Roadmap from current baseline

### Completed milestones (reported)

- Foundation: private repo, rules/settings, five initial Skills, Git workflow, GitHub Actions and documentation.
- Expanded capability-based Skills: design assistance, calculations, component engineering selection, distributor stock sourcing, component checking, schematic review, PCB review, and lightweight debug assistance.
- Schematic inspection **Stable (Scoped)**: nine commands, hardening, regression/golden testing, targeted native KiCad comparison.
- PCB inspection **Stable (Scoped)**: eight commands, hardening, regression/golden testing, real board read-only checks.
- Real-project skill exercises and **repository-level integration audit: PASS**.

### Next — recommended operating phase

**Priority A: Practical adoption & bug maintenance**

- Use the assistant across several existing projects (power, digital, mixed-signal), especially with different schematic hierarchy, PCB footprints and workflows.
- Record only meaningful reproducible problems: failed routing, inaccurate outputs, misleading confidence, excessive context, unsupported cases that materially block work.
- Fix confirmed issues with regression protection; avoid expanding KiCad parsers simply because more KiCad object types exist.

**Priority B: Trustworthiness and ergonomics**

- Verify intended automatic skill selection vs unneeded skill loading in practical tasks.
- Validate sourcing results against up-to-date stock and manufacturer documentation; keep distributor/assembly stock distinct.
- Verify actual CI results on the latest branch/commit; keep synthetic and golden test status separate.
- Check portability by running on macOS when accessible; no need to claim untested parity.
- Monitor context/token efficiency qualitatively or with measurements before introducing optimization machinery.

**Priority C: Conditional improvements only when justified**

- Better examples/short prompts or skill descriptions if real tasks reveal routing problems.
- Targeted support for recurring high-value gaps in component selection or diagnostics, **without** hardcoding device categories into generic Skills.
- Additional golden projects/negative cases if they catch a real failure mode.
- New agents/skills only if distinct isolation or context needs justify the complexity; no obligatory expansion.

### Explicitly deferred or excluded

- No new inspection CLI commands beyond the agreed 9 SCH and 8 PCB without re-scoping.
- No rewrite of KiCad ERC/DRC or copper/zone connectivity engines.
- No formal review stages/gates, automatic release-state mutation or dependence on Hardware Review Framework.
- No installer, migration framework, checksum/SHA manifests or release tag by default.
- No automatic circuit modifications or online purchasing.

## 11. Open limitations / unresolved verification

| Topic | Status / consequence |
|---|---|
| Native macOS runtime for inspection scripts | Not independently confirmed in reported acceptance; test when machine available |
| OS-enforced read-only sandbox | Not verified; instruction/policy and hash tests are not OS access controls |
| SCH bus expansion, symbol inheritance, hidden connectivity, complex sheet reuse | Intentional `NOT_VERIFIED` scope |
| PCB actual filled copper/clearance/DRC/complete return paths | Intentional `NOT_VERIFIED` scope; use native tools and targeted human inspection |
| Stock, lifecycle and lead time | Dynamic data; must be checked against current supplier/manufacturer sources when used |
| Unsaved KiCad GUI state | Query scripts reflect saved on-disk files only |
| Exact most recent branch HEAD / post-documentation CI | Not available in this record; inspect GitHub/local repo |

## 12. Minimal handoff context for a new assistant session

> Project: **Hardware-Copilot**, independent private GitHub repo for a general-purpose Claude Code hardware engineering assistant. Design is capability-based rather than device-specific. Use `.claude/rules/` and on-demand `.claude/skills/`; manually copy Skills into other KiCad projects. KiCad native design files remain strictly read-only, local `hardware/` is gitignored, and no auto installer, SHA/checksum manifest or Git tag is desired. `sch-inspect` v1.0 (9 commands) and `pcb-inspect` v1.0 (8 commands) are Stable (Scoped). Reported final synthetic tests: SCH 21/21, PCB 31/31; golden SCH 5/5, PCB 2/2; repo integration audit PASS. Other design, calculation, component, sourcing, review and debug Skills were exercised successfully in scoped tasks. Do not conflate PCB net assignments with copper connectivity, and propagate `NOT_VERIFIED` when native KiCad, manufacturer or current supply-chain evidence is insufficient. Next priority is real project adoption, narrow bug fixes and verified CI/current stock data; no speculative feature creep.

---

**Maintenance note:** Update this file only when an important project decision, scope/validation result or roadmap priority changes. Keep it as concise continuity material rather than an automatic session transcript; do not treat it as live authoritative code or repository state.
