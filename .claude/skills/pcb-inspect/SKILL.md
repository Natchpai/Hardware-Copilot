---
name: pcb-inspect
description: >-
  Inspects and explains KiCad 10 PCB layout data in read-only mode.
  Use when the user asks to review, inspect, troubleshoot, or verify
  component placement, footprints, pads, nets, traces, vias, copper
  zones, layers, clearances, or a specific board area. Prefer targeted
  native .kicad_pcb inspection rather than loading the whole board.
argument-hint: "[summary | footprint <ref> | net <name> | area <target> | check [target]]"
---

# PCB Inspection

## Scope and safety
- Read-only: do not modify PCB, project, library, or design-rule files.
- Operate independently of any formal review framework.
- Treat the saved `.kicad_pcb` as the file-based source of truth; disclose if unsaved editor changes may exist.
- Never claim that a check passed unless supporting data and the check method are available.
- Do not assume a PCB inspection tool, parser, IPC connection, or local DRC capability exists; verify tools before using them.

## Available read-only CLI (v0.1)

Use `scripts/query_pcb.py` with Python 3.10+ standard library:

- `python scripts/query_pcb.py summary --board <file.kicad_pcb> [--limit 20]`
- `python scripts/query_pcb.py footprint <ref> --board <file.kicad_pcb> [--limit 20]`

`summary` reports board metadata, declared layers, footprint counts, and bounded footprint samples.
`footprint` reports saved footprint reference/value, library ID, side/layer, placement,
rotation, and UUID. If a reference has multiple matches, report `AMBIGUOUS_REFERENCE`.
These outputs are structural evidence only: no pad nets, electrical connectivity,
track/via geometry, copper fill, manufacturing or DRC verification is implemented.
Never claim a planned mode is an implemented CLI command.

## Planned inspection modes (not yet implemented as CLI)
- `component <ref>`: future extended footprint, pads, assigned nets, placement, and relevant neighboring routing.
- `net <name>`: inspect relevant pads, tracks, vias, and layers; expand along the net only as needed.
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
