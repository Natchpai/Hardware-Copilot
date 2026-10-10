---
name: sch-inspect
description: >-
  Inspects and analyzes KiCad 10 schematic designs using native
  .kicad_sch files. Use when the user asks to inspect, review,
  verify, troubleshoot, or explain schematic circuits,
  components, pins, nets, connectivity, hierarchical sheets,
  or functional blocks. Supports targeted, read-only
  inspection without loading the entire project.
argument-hint: "[component <ref> | net <name> | block <sheet> | check [sheet]]"
---

# Schematic Inspection (KiCad 10)

## Invocation
Interpret `$ARGUMENTS` as one of:
- `component <reference>` — inspect a symbol instance and its local connections.
- `net <name>` — inspect a named net with an explicit connectivity scope.
- `block <sheet-file-or-name>` — inspect one hierarchical sheet and its interfaces.
- `check [sheet-file-or-name]` — perform targeted structural checks; ERC only when requested or clearly necessary.

If no mode is given, ask for a target or offer these four modes. Do not default to a full-project scan.

## Non-negotiable rules
- Treat `.kicad_sch`, `.kicad_pro`, libraries, and all other CAD source files as read-only. Do not change review state.
- Start with the requested sheet/instance; minimize files read and information returned to context.
- Do **not** export or ingest a whole-project netlist as the default inspection method.
- Prefer a tested local read-only S-expression query/parser when available. Never imply a parser, connectivity resolver, or ERC check exists if it has not been run.
- Do not mistake text search, matching net labels, or nearby wires for electrically proven connectivity.
- Never claim PASS where the requested check is incomplete; use `NOT_VERIFIED` with the missing evidence.
- Do not create indexes, reports, caches, or other persistent artifacts unless explicitly requested.

## Procedure
1. **Locate:** Identify the project root and the requested sheet or symbol instance. Use filenames and a bounded reference/sheet lookup; do not display raw full-sheet contents to the model.
2. **Identify instance:** Resolve the correct hierarchical instance path, especially for reused sheet files and multi-unit symbols. If ambiguous, report candidate instances and request a selection.
3. **Inspect locally:** Use structured, bounded results for symbols, reference/value, pins, labels, wires, junctions, no-connect markers, and immediate neighbors from the target `.kicad_sch`.
4. **Assess connectivity:** Separate directly evidenced local connectivity from inferred or unresolved connections. Include power symbols and implicit/global connectivity only if the tool resolves their semantics correctly.
5. **Expand conditionally:** Follow parent/child sheet pins, hierarchical labels, global labels, or power nets only as needed. Do not treat a repeated local label in separate sheet instances as globally connected.
6. **Validate:** Use supported calculations, datasheet evidence, or targeted checks relevant to the question. Do not claim schematic/ERC correctness from a partial parse.
7. **Report:** Return concise observations with file, sheet instance, reference, pin/net, evidence, scope, and follow-up actions.

## Scope and evidence
- `LOCAL`: only the selected sheet instance and locally established connections.
- `HIERARCHICAL`: includes traced parent/child hierarchical interfaces.
- `GLOBAL`: includes relevant global labels/power connectivity across the project; report which sources were consulted.
- Report the **actual** verified scope, not the user's requested scope when expansion could not be completed.
- `PASS` requires sufficient validated evidence for the specific check; otherwise use `WARNING`, `FAIL`, or `NOT_VERIFIED` as appropriate. Distinguish an observed issue from a suspected issue.

## Tool fallback
- If no trustworthy local `.kicad_sch` parser/query tool exists, limit work to transparent structural observations from the *target* sheet and targeted excerpts. Mark unproven pin-to-net and cross-sheet claims `NOT_VERIFIED`.
- Do not silently replace the sheet-scoped workflow with full-project `kicad-cli` netlist export. If a project-wide connectivity proof is essential, explain the limitation and request explicit permission for an alternative verification route.
- ERC is a distinct optional verification step; if run, label its exact scope and output, and do not equate ERC success with circuit correctness.

## Response format
- **Target & scope:** file, sheet instance, requested object; `LOCAL` / `HIERARCHICAL` / `GLOBAL`.
- **Findings:** brief result(s) with reference/pin/net and traceable evidence.
- **Not verified:** unresolved connectivity, missing data, or tool limitations.
- **Next action:** focused verification or human visual check, only if needed.

## Supporting References
- For native schematic structure, hierarchy, and evidence rules,
  read [Schematic Data Reference](references/schematic-data.md)
  only when needed.


## Available Tools

Use `scripts/query_sch.py` for targeted, read-only inspection
of native KiCad 10 `.kicad_sch` files.

### Supported Commands

| Command | Purpose |
|---|---|
| `summary` | Summarize schematic sheets and component counts. |
| `component <ref>` | Locate a component and inspect its properties. |
| `sheet <name>` | Locate a hierarchical sheet. |
| `pins <ref>` | Inspect symbol pins and local wire/label geometry. |
| `local-net <ref>` | Trace sheet-local wires, junctions, labels, and power symbols. |
| `hier-net <ref>` | Trace hierarchical interfaces to parent sheet connections. |
| `connected-pins <ref>` | Discover connected component and sheet pins across supported hierarchy paths. |
| `instances` | Inspect hierarchical sheet instances and reused sheet files. |
| `project-net <ref> --pin <number>` | Trace connectivity evidence across sheet instances, global labels, and power nets. |

### Usage

Run with an available Python 3 interpreter:

`python scripts/query_sch.py <command> [target] --project <root.kicad_sch>`

Examples:
- `python scripts/query_sch.py component U103 --project Top_hierarchical.kicad_sch`
- `python scripts/query_sch.py connected-pins U103 --project Top_hierarchical.kicad_sch`
- `python scripts/query_sch.py project-net U103 --pin 8 --project Top_hierarchical.kicad_sch`

Resolve script and project paths before execution.
Do not assume the current working directory.
Maintain Windows and macOS compatibility.

### Inspection Policy

- Prefer `component`, `pins`, or `local-net` for targeted inspections.
- Use `hier-net` or `connected-pins` when hierarchy traversal is needed.
- Use `project-net` only when project-level connectivity evidence is required.
- Select a specific pin when the component contains multiple independent nets.
- Read JSON output selectively; avoid loading full CAD files into context.
- Do not export full-project netlists by default.
- Never modify schematic or library files.

### JSON Contract

- Every successful command returns the bounded envelope `mode`, `target`, `root`,
  `results`, `total_matches`, `truncated`, `missing_sheets`,
  `skipped_outside_project`, `verification`, `limitations`, and `warnings`.
- `project-net` returns one result with either
  `status: PROJECT_CONNECTIVITY_EVIDENCE` and its source pin, connected pins,
  label/power evidence, truncation flags, and limitations; or an unresolved
  status: `TARGET_NOT_FOUND_OR_UNRESOLVED` or `AMBIGUOUS_TARGET_NETS`.
  Report either unresolved status as `NOT_VERIFIED`; it does not prove that a
  connection is absent. Its `project_net_verified` field is always false: it
  is not a KiCad-netlist-parity claim.
- Invalid input, unreadable files, unsupported bounds, or traversal failures
  exit nonzero and emit JSON with `verification: NOT_VERIFIED`. Do not infer
  connectivity from that error result.
- Honor `truncated`, `pins_truncated`, `connected_pins_truncated`, and
  `names_truncated`; a truncated result is not a complete net enumeration.

### Verification Limitations

- Local geometry does not establish complete electrical correctness.
- `project-net` provides connectivity evidence, not verified KiCad netlist parity.
- Global labels and power symbols may connect nets across sheet instances.
- Complex symbol inheritance, buses, and hidden connectivity may remain unresolved.
- Never interpret an empty result as proof that a connection does not exist.
- Report incomplete or unsupported verification as `NOT_VERIFIED`.

## Tool Limitations

- `summary`, `component`, and `sheet` provide structural discovery only.
- `pins` and `local-net` provide local geometry evidence; `hier-net` and
  `connected-pins` provide bounded parent/interface geometry evidence.
- `project-net` provides conservative, instance-aware project connectivity
  evidence through supported wires, labels, hierarchy, global labels, and
  power symbols. It is explicitly not verified KiCad netlist parity.
- Never infer electrical correctness from structural or geometry evidence.
- Report unsupported checks as NOT_VERIFIED.
- Do not export full-project netlists as a fallback.
- If the tool fails, report the failure instead of guessing.
- Resolve the script and project paths before execution.
- Do not assume the current working directory.
- Preserve cross-platform compatibility (Windows/macOS).
