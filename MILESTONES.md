# Milestones

Planned work for the skills in this repo. One section per milestone. Tick a
task when its change is merged, and move finished milestones to the bottom.

## M2: pcb-inspect 1.1 (back-side fix, KiCad 10 nets, net totals)

Status: done in v3.3.0 (PRs #24, #25 and the 1.1 release PR). Checked on one
of the two boards; the 482-footprint board was not available for this work.
Scope: `.claude/skills/pcb-inspect/` only
Source: review of `query_pcb.py` on 2026-11-10, run against two routed
KiCad 10 boards (file version 20260206): one with 306 footprints, 1599
segments, 797 vias and 133 zones, and one with 482 footprints. All 31 unit
tests passed before this work.

Goal: fix wrong pad centres on the back side, stop flagging the normal
KiCad 10 net format as unverified, and answer per-net questions without
dumping every segment.

### Tasks

Task 1 is a confirmed defect and comes first. The rest are ordered by value.

- [x] **1. Remove the extra B.Cu mirror in `board_position`.**
  `scripts/query_pcb.py:329` negates the pad's local X for a footprint on
  `B.Cu`. The saved file already stores flipped local coordinates, so the
  script mirrors twice. Evidence: on the 306-footprint board, back-side pad
  centres were compared with track ends and via centres on the same net
  (0.05 mm tolerance, pads with local X = 0 left out). Without the mirror 38
  of 45 pads matched. With the script's mirror 2 of 45 matched. Front-side
  pads matched at the same rate both ways (500 of 679).
  Effect: `pads` and `pad-distance` report wrong positions for every
  back-side part with an off-centre pad, labelled `STRUCTURAL_EVIDENCE`.
  A distance between two pads of the same footprint is still right.
  `test_pads_applies_back_layer_mirror_and_rotation` and
  `test_pad_distance_uses_rotated_back_layer_and_unusual_reference_transforms`
  encode the wrong behaviour, and the golden test only covers a front-side
  resistor at 0 degrees.
  Done when: the mirror is removed, both tests use expected values taken
  from a board saved by KiCad 10 with a back-side part at 0 and at 90
  degrees, the golden evidence file gains one back-side pad, and
  `references/cli.md` and the limitation strings no longer say "B.Cu mirror
  transform".

- [x] **2. Treat name-only nets as the normal KiCad 10 format.**
  KiCad 10 boards have no net table and store `(net "name")` on each item.
  Both test boards had 0 declared nets, so every pad, track and via reports
  `ASSIGNED_WITHOUT_DECLARATION` and `net_declaration_status: NOT_VERIFIED`
  (`scripts/query_pcb.py:167`). That is noise on every query and hides real
  `NOT_VERIFIED` results.
  Done when: a board with no net table reports `ASSIGNED` for name-only
  nets, `ASSIGNED_WITHOUT_DECLARATION` is kept only for a board that has a
  net table but is missing that entry, and `SKILL.md` and `cli.md` say so.

- [x] **3. Add per-net totals to `tracks` and `vias`.**
  Output is a list cut at `--limit`. To get total length the agent must
  raise the limit and add up segments in context.
  Done when: `tracks` also returns, over all matches and not only the
  listed ones, segment count, total length, length per layer, and the set of
  widths with a count each. `vias` returns a count per size, drill and layer
  span. The existing note that this is not routed-path length stays.

- [x] **4. Add a `zones <net>` command.**
  Zones are skipped by `scan_board`. One test board has 133. Power and
  ground questions cannot be answered without them.
  Done when: `zones <net>` returns layer, net, name, priority, outline
  bounding box, clearance and connect-pad settings, and whether saved fill
  polygons exist, with fill state marked `NOT_VERIFIED`.

- [x] **5. Add a `nets` command and board totals in `summary`.**
  There is no way to list or search net names, so the agent must already
  know the exact name, including the sheet path prefix such as
  `/Top/Power Supplies/+5VUSB`.
  Done when: `nets [--match <text>]` lists names with pad, track and via
  counts, and `summary` adds net, track, via and zone counts and the
  `Edge.Cuts` bounding box.

- [x] **6. Add `--layer` and `--radius` filters to `nearby`.**
  `nearby` ranks every footprint on both sides by origin distance.
  Done when: both filters work, and the output says which were applied.

- [x] **7. Make version and output conventions consistent.**
  `SKILL.md` says "v1.0, Stable (Scoped)" and the script docstring says
  "v0.4" (`scripts/query_pcb.py:2`). Errors go to stdout here and to stderr
  in `query_sch.py`.
  Done when: one version string is used in both files, and both scripts
  send error JSON to the same stream.

- [x] **8. Make the golden tests configurable per project.**
  `tests/test_query_pcb_golden.py` and
  `references/2phase-synchbuck-golden-evidence.md` belong to one project.
  Do this together with M1 task 8, with the same JSON format.
  Done when: expected values come from a file named by an environment
  variable, and the project-specific evidence file is moved out of the
  skill or marked as an example.

### Out of scope

- Copper continuity, clearance and DRC. A shared net stays an assignment
  lookup.
- Pad outlines and custom pad shapes. They stay `NOT_VERIFIED`.
- Zone fill correctness and stackup.
- Any write to a KiCad file.

### Exit criteria

- All tasks ticked or moved to a later milestone with a reason.
- Unit tests pass on Windows and macOS in CI.
- A synthetic test was added before each parser fix (see `CONTRIBUTING.md`).
- `version` in `.claude-plugin/plugin.json` is bumped.

## M3: sch-review 1.1 (requirements, pin coverage, rule conflicts)

Status: tasks and exit criteria done on `feat/sch-review-1.1`, not merged.
The real block review was the `MCU_power` sheet of the 2-phase buck project
on 2026-11-11, read by the engineer. It found that pin status comes from
`local-net`, not `pins`; step 3 was fixed.
Scope: `.claude/skills/sch-review/SKILL.md` (the skill has no script)
Source: read-through on 2026-11-10 against `.claude/rules/engineering.md`,
`.claude/rules/pdf.md` and `sch-inspect`. The skill was not run on a real
review, so these are text findings, not observed failures.

Goal: make a review check the design against its requirements and account
for every pin, and remove the places where the skill disagrees with the
rules.

### Tasks

- [x] **1. Check against the project's requirements.**
  Workflow step 1 takes function and operating range from the user or from
  assumptions. It never says to read the project's specification, so a
  review can miss "does this meet the requirement".
  Done when: step 1 says to find the specification or requirements record if
  the project has one, read the entries for the block in scope, and cite the
  requirement, decision or open-item ID in each finding it relates to. With
  no such record, the operating range is `ASSUMED` and stated.

- [x] **2. Add a pin coverage step.**
  "Floating pins" is one word in a list in step 4. Accounting for every pin
  of each IC in scope is the most mechanical check in a schematic review,
  and `sch-inspect pins` gives the data.
  Done when: the workflow has a step that lists, for each IC in scope, every
  pin as connected, marked no-connect, or unresolved, and compares
  no-connect and strap pins with the datasheet. Unresolved pins go to the
  `NOT_VERIFIED` section.

- [x] **3. Fix the NotebookLM and PDF wording.**
  Lines 44 to 47 say "Never open or read a PDF" and that NotebookLM answers
  are "used only after the user approves uploading the file". `pdf.md`
  allows reading project report PDFs, and lets an existing notebook be
  queried without asking. Approval is only for adding a source. The current
  text can make the agent ask before every query.
  Done when: the text says datasheet, schematic and PCB PDFs are not read,
  an existing notebook is queried without asking, and adding a source needs
  approval.

- [x] **4. Use one finding format.**
  `engineering.md` defines five fields. The skill's row has eight, and it
  adds a status whose value `NOT_VERIFIED` is also an evidence label, so a
  row can read `NOT_VERIFIED | NOT_VERIFIED`. The example row shows
  `Potential risk | VERIFIED` with no note on what each one rates.
  Done when: the row is the `engineering.md` format plus named extra fields,
  the status values are Confirmed defect, Potential risk and Undecided, and
  one sentence says the evidence label rates the observation and the status
  rates the conclusion.

- [x] **5. Remove the repeated read-only rule.**
  "KiCad files are read-only, propose changes, do not apply" is stated in
  Boundaries (line 20) and again in Evidence baseline (line 48).
  Done when: it is stated once. Keep the evidence labels and severity
  definitions, because the skill must work when copied alone.

- [x] **6. Say what to do for a sheet-level target.**
  The argument hint offers `sheet`, but `sch-inspect` cannot list the
  components on a sheet, so the agent has no stated way to start.
  M1 task 2 added `components --sheet`. Asking for the references or
  reading the sheet's symbol list stays as the fallback without `sch-inspect`.
  Done when: step 2 names the command for each target type (sheet,
  subsystem, reference, concern).

- [x] **7. Add the saved-file note.**
  `pcb-inspect` says the saved file may differ from the open editor. This
  skill does not.
  Done when: Boundaries says the review covers the saved files, and that a
  `.lck` file means the editor may hold unsaved changes.

- [x] **8. Add three evaluation prompts.**
  There is no test for a prompt-only skill.
  Done when: the repo has three short cases with expected behaviour: a
  block with a known defect, a block with missing constraints (should give
  `ASSUMED` and `NOT_VERIFIED`, not a pass), and a lookup-only question
  (should not trigger this skill).

### Out of scope

- A fixed checklist per topology or device family. The skill stays
  risk-based.
- ERC, simulation and measurement. They stay separate activities.

### Exit criteria

- All tasks ticked or moved to a later milestone with a reason.
- The skill still works when copied alone, without `.claude/rules/`.
- One real block review was run with the new text and read by the engineer.

## M1: sch-inspect 1.1 (net queries and contract cleanup)

Status: done in v3.2.0 (PRs #20, #21 and the 1.1 release PR). One part of
task 5 moved to a later milestone, see below.
Scope: `.claude/skills/sch-inspect/` only
Source: review of `query_sch.py` v1.0.1 on 2026-11-10, run against a real
KiCad 10 project (5 sheets, 78 symbols). All 21 unit tests passed before this
work.

Goal: let a user start from a net name or a sheet, not only from a reference
and pin, and make `SKILL.md` match what the script prints.

### Tasks

Ordered by value. Tasks 1 and 2 change daily use the most.

- [x] **1. Add a `net <name>` command.**
  Today a query can only start from a reference and pin, so "what is on
  `+5V`?" needs a known pin on that net. `CLAUDE.md` tells users to query by
  "sheet, ref, net", and the skill cannot do the last one.
  Done when: `net <name>` returns the component pins reached from every local
  label, global label, hierarchical label and power symbol with that name,
  with the same instance-aware evidence and truncation flags as `project-net`.
  A local label name that exists in several sheet instances returns one result
  per instance, not one merged net.

- [x] **2. Add a `components` command with `--sheet` and `--prefix` filters.**
  `SKILL.md` says there is no way to list or search components, so the agent
  has to ask or guess designators.
  Done when: `components --sheet <name> --prefix U` lists reference, value,
  `lib_id` and instance path, bounded by `--limit`, and the "no command to
  list" paragraph is removed from `SKILL.md`.

- [x] **3. Fix the top-level `limitations` for `project-net` and `instances`.**
  Both fall into the `summary` branch (`scripts/query_sch.py:1023`) and print
  "No electrical connectivity or pin-net verification" and "Shared sheet files
  are not expanded into unique hierarchical instances". That is wrong for
  both. `SKILL.md` works around it with "A generic limitation line in
  `project-net` output does not override its instance-aware evidence".
  Done when: each mode prints its own limitations, a test checks them, and the
  workaround sentence is deleted.

- [x] **4. Make the `verification` values in `SKILL.md` match the script.**
  The script also emits `SHEET_LOCAL_ONLY`,
  `HIERARCHICAL_INTERFACE_EVIDENCE_ONLY`,
  `PARENT_CONNECTED_PINS_GEOMETRY_ONLY` and
  `HIERARCHICAL_INSTANCE_DISCOVERY_ONLY` (`scripts/query_sch.py:1016`). The
  JSON contract section lists none of them.
  Done when: the contract lists every value the script can print, one per
  command, and a test fails if a new value is added without a doc update.

- [x] **5. Test mirror combined with 90 and 270 degree rotation.**
  `pins_from_symbol` applies the mirror before the rotation
  (`scripts/query_sch.py:287`). The two only commute at 0 and 180 degrees, and
  the tests contain no mirrored symbol. A wrong order gives silently missing
  connections. Status today: `NOT_VERIFIED`.
  Done when: fixtures cover `mirror x` and `mirror y` at 90 and 270 degrees,
  with expected pin positions taken from a file saved by KiCad 10, not from
  the script's own output.
  Result: confirmed defect, fixed. `mirror x` at 90 and 270 degrees swapped
  pins 1 and 2. Checked on a real project against a netlist exported by
  kicad-cli 10.0.8, through the golden tests. No repo fixture was added.

- [x] **6. Join a global label and a power symbol that share a name.**
  `global_nodes` and `power_nodes` are joined separately
  (`scripts/query_sch.py:868`). KiCad joins them by name.
  Done when: a fixture with global label `VBUS` on one sheet and power symbol
  `VBUS` on another reports one net, and `PWR_FLAG` still joins nothing.

- [x] **7. Detect power symbols the same way everywhere.**
  `power_symbol_anchors` uses the `(power)` flag of the library symbol, but
  `project_connections` hides power pins by the `power:` library prefix
  (`scripts/query_sch.py:823`). A power symbol kept in a project library, for
  example `0_Power:GND`, shows up as a component pin.
  Done when: both places use the `(power)` flag, with a fixture for a power
  symbol outside the `power` library.

- [x] **8. Make the golden tests configurable per project.**
  `tests/test_query_sch_golden.py` hard-codes one project's values
  (`U103`, `R506`, `+9V`, sheet names "Power State" and "MCU IOs"). In any
  other project they skip, or fail if `KICAD_GOLDEN_PROJECT` is set.
  Done when: expected values come from a small JSON file named by an
  environment variable, the README section "Tests and CI" explains the format,
  and the tests skip cleanly when the file is not set.

- [x] **9. Trim `SKILL.md` and `references/schematic-data.md`.**
  "Not netlist parity" and "use `NOT_VERIFIED`" are stated in Rules, Scope
  levels, JSON contract and Limitations, and the reference file repeats the
  scope levels and the contract.
  Done when: each rule is stated once, the reference file keeps only the
  native file structure notes, and no behaviour rule is lost. Use the
  `writing-for-agents` skill for the pass. Do this after tasks 1 to 4, since
  they change the same text.

- [x] **10. Parse each file once per query.**
  A file is read and parsed again in `read_sheet`, `local_geometry`,
  `power_symbol_anchors`, `inspect_pins` and `connected_parent_pins`, and
  `resolve_local_networks` compares every anchor with every wire. A 78-symbol
  sheet takes about 0.1 s, so this is not urgent. It will matter on sheets
  with large MCUs.
  Done when: one parse per file per run, output is byte-identical on the
  existing fixtures, and the time on a large sheet is recorded in the PR.

### Out of scope

- KiCad netlist parity. `project_net_verified` stays false.
- Bus expansion and bus entries.
- Hidden power pins and other implicit connections.
- Any write to a KiCad file.

### Moved to a later milestone

- **Task 5, `mirror y` at 90 and 270 degrees.** The fix applies the same
  rule to `mirror y`, but the test project has no such part, so it is
  `NOT_VERIFIED`. Needs a KiCad 10 saved file with a `mirror y` symbol at 90
  and at 270 degrees. `SKILL.md` tells the agent to treat those pin-net
  results as `NOT_VERIFIED` until then.

### Exit criteria

- All tasks ticked or moved to a later milestone with a reason.
- Unit tests pass on Windows and macOS in CI.
- A synthetic test was added before each parser fix (see `CONTRIBUTING.md`).
- `version` in `.claude-plugin/plugin.json` and the version in the
  `query_sch.py` docstring are bumped.
