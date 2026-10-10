---
name: pcb-inspect
description: >-
  Inspects and explains KiCad 10 PCB layout data in read-only mode.
  Use when the user asks to review, inspect, troubleshoot, or verify
  component placement, footprints, pads, nets, traces, vias, copper
  zones, layers, clearances, or a specific board area. Prefer targeted
  native .kicad_pcb inspection rather than loading the whole board.
argument-hint: "[summary | footprint <ref> | pads <ref> | net <name> | tracks <net> | vias <net> | nearby <ref> | pad-distance <ref.pin> <ref.pin>]"
---

# PCB Inspection

## Scope and safety
- Read-only: do not modify PCB, project, library, or design-rule files.
- Operate independently of any formal review framework.
- Treat the saved `.kicad_pcb` as the file-based source of truth; disclose if unsaved editor changes may exist.
- Never claim that a check passed unless supporting data and the check method are available.
- Do not assume a PCB inspection tool, parser, IPC connection, or local DRC capability exists; verify tools before using them.

## Available read-only CLI (v1.0 — Stable (Scoped))

Use `scripts/query_pcb.py` with Python 3.10+ standard library:

- `python scripts/query_pcb.py summary --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py footprint <ref> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py pads <ref> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py net <name> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py tracks <net> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py vias <net> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py nearby <ref> --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py pad-distance <ref.pin> <ref.pin> --board <file.kicad_pcb> [--limit 20]`

`summary` reports board metadata, declared layers, footprint counts, and bounded footprint samples.
`footprint` reports saved footprint reference/value, library ID, side/layer, placement,
rotation, and UUID. If a reference has multiple matches, report `AMBIGUOUS_REFERENCE`.
`pads` reports saved pad numbers, types, shapes, declared layers, nominal sizes, saved
net assignment, and board-space pad centres. It supports SMD and through-hole pads,
including footprint translation, rotation, and B.Cu mirroring. Unconnected pads are
reported as `UNCONNECTED`; a custom or unsupported pad outline is `NOT_VERIFIED`.
`net` reports a declared net's assigned footprint/pad records. A net absent from the
saved assignments is `MISSING`. KiCad files that store a name-only pad assignment without
a declared net table are reported as `ASSIGNED_WITHOUT_DECLARATION` with declaration
semantics `NOT_VERIFIED`. Matching saved net names are an assignment lookup only, not
evidence of copper connectivity.
`tracks` reports saved straight segments and arcs assigned to one exact net, including
layer, width, start/end coordinates, and geometric length in millimeters. Arc records
also include their saved `mid` point. A zero-length segment is reported as `0.0`; a
missing or malformed geometry, or an arc that cannot be resolved from its three points,
has `length_mm: null` and `length_status: NOT_VERIFIED` rather than an estimate.
`vias` reports saved net assignment, board-space position, size, drill, layer span, and
the saved via type when present. An omitted via type is `null` with
`via_type_status: NOT_VERIFIED`; it is not assumed to be through-hole.
`nearby` reports all other saved footprints ordered by Euclidean distance from the
requested footprint's saved origin, in board coordinates. The queried footprint is not
included as its own neighbor. `origin`, each neighbor origin, and `distance_mm` explicitly
identify the measurement points; no package outline or copper geometry is used.
`pad-distance` reports the Euclidean distance between two uniquely resolved saved pad
centres after the existing footprint rotation and B.Cu mirror transforms. Pad identifiers
are matched against complete saved references before their exact pad numbers, so references
and pad numbers may themselves contain dots or other unusual characters. A requested
identifier that resolves to multiple saved pads returns `AMBIGUOUS`; missing or unresolvable
saved geometry returns structured `NOT_FOUND` or `NOT_VERIFIED` JSON without a distance.
Malformed saved S-expressions, conflicting net declarations, malformed geometry, and
unresolvable coordinates return structured `NOT_VERIFIED` JSON; they do not fall back to
guessed geometry. Duplicate references retain `AMBIGUOUS_REFERENCE`; a pad identifier that
matches more than one saved pad returns `AMBIGUOUS` with a bounded candidate list.

For `tracks` and `vias`, an empty quoted target (`""`) requests explicitly unconnected
items. `MISSING`, `UNCONNECTED`, and `ASSIGNED_WITHOUT_DECLARATION` are distinct saved
assignment states. A declared net with no matching routing items returns `NOT_FOUND` with
`net_status: DECLARED`.

Output is bounded by `--limit` (1 through 1000) and JSON object keys plus result lists
have deterministic ordering. The CLI never infers physical copper connectivity,
clearance, route completeness, signal-path length, filled zones, or electrical continuity
from an assigned net name or geometric distance. Never claim a planned mode is an
implemented CLI command.

## Regression and golden validation

Run synthetic tests with:

- `python tests/run_tests.py --pattern test_query_pcb.py --label synthetic`

For opt-in project evidence, set `KICAD_PCB_GOLDEN_BOARD` to an absolute
`.kicad_pcb` path, then run:

- `python tests/run_tests.py --pattern test_query_pcb_golden.py --label golden`

Golden tests skip when the environment variable is absent and fail when it is explicitly
configured to a missing or non-PCB path. The 2Phase_SynchBuck values are independently
transcribed from native KiCad PCB text and checked against this read-only CLI; they are not
derived from a previous CLI result. See
`references/2phase-synchbuck-golden-evidence.md` for the recorded native evidence.
Golden coverage is intentionally narrow and does not claim complete PCB Editor, DRC, or
connectivity parity.

## Planned inspection modes (not yet implemented as CLI)
- `component <ref>`: future extended footprint, pads, assigned nets, placement, and relevant neighboring routing.
- `area <target>`: inspect a reference-centered region or explicit board coordinates (millimeters); state the bounds used.
- `check [target]`: inspect requested structural constraints or available DRC results. Full-board DRC is not a local check; filtering findings by target does not make it local DRC.
- If no explicit mode is given, infer the smallest useful scope from the request.

## Procedure
1. Identify the project, requested target, inspection question, and scope.
2. Locate the target with the least expensive available read-only method.
3. Prefer native `.kicad_pcb` or supported read-only KiCad API queries. Use a verified local query script if installed; do not invent one.
4. Return only relevant geometry and connectivity: footprints/pads, nets, tracks/vias, layer assignments, zones, and applicable constraints.
5. Analyze relevant electrical and physical risks. Expand to connected regions, stackup data, or datasheet guidance only when needed.
6. If structural data is insufficient, request a targeted visual inspection rather than exporting images of the entire board.
7. Provide concise findings with references, net names, layer names, coordinates, evidence, and unresolved checks.

## Verification boundaries
- Distinguish saved zone outlines from filled copper; do not assume fills are current.
- DRC results do not establish signal integrity, power integrity, EMI, thermal performance, or manufacturability.
- Distance alone does not prove decoupling effectiveness; consider actual connections and return paths.
- Footprint-origin and pad-centre distances do not measure package clearances, copper clearances, routed path length, or electrical behavior.
- Track lengths are individual saved geometric primitives only; they are not a routed-path, return-path, or timing-length measurement.
- Via geometry and a shared net assignment do not prove the via contacts any particular track, pad, copper zone, or layer.
- Unrecognized KiCad constructs, filled-zone state, board stackup, actual copper contact, and any geometry that cannot be parsed safely remain `NOT_VERIFIED`.
- If geometry, connectivity, stackup, or tool coverage is insufficient, mark that question `NOT_VERIFIED`.
- Never interpret absence of a reported violation as proof of correctness.

## Context and output
- Never put the complete board file, full track list, or unfiltered DRC report in context by default.
- Limit results to the requested target and summarize large result sets; state truncation and offer scoped expansion.
- Output: **Target / Scope**, **Findings**, **Evidence**, **Limitations / NOT_VERIFIED**, **Recommended next checks**.
- Do not create reports, temporary exports, caches, or other persistent files unless specifically authorized.

## Optional supporting files
- When added, load supporting references only for the relevant inspection question.
- Run a verified read-only query tool when available, and review its summarized output instead of its entire source or raw board data.
