---
name: pcb-review
description: >-
  Perform evidence-based, read-only PCB layout reviews for KiCad designs.
  Use when the user asks to assess layout risks, placement, routing, power,
  thermal, signal-integrity, or manufacturability concerns in a PCB design.
argument-hint: "[board, area, net, reference, or review concern]"
---

# PCB Layout Review

Review the requested scope as an engineering assessment, not a formal approval
or design-state transition. Native KiCad files are authoritative; Human
engineers retain final design authority. Do not modify PCB, library, project,
or review files.

## Scope and evidence

Start from the project's requirements, operating conditions, constraints, and
the user's review question. Select the smallest useful focus: a board area,
power domain, interface, component group, net, or manufacturing risk. Do not
apply a fixed circuit-type checklist or assume an architecture from reference
designators or net names.

Use `pcb-inspect` for targeted saved-board evidence:

- `summary`, `footprint`, and `nearby` for placement context.
- `pads` and `pad-distance` for transformed pad-centre geometry and assignments.
- `net` for saved pad assignments only.
- `tracks` and `vias` for saved routing primitive geometry and metadata.

Respect its bounded output, ambiguity results, and `NOT_VERIFIED` states. A
shared net name, track assignment, via assignment, or geometric distance does
not prove copper continuity, clearance, route completeness, return-path quality,
or electrical behavior.

Results reflect the saved `.kicad_pcb` file, not unsaved edits
in KiCad PCB Editor. Report editor-state consistency as
`NOT_VERIFIED` unless independently checked.

Use `component-check` and authoritative datasheets only when exact part,
package, rating, pinout, thermal, or layout guidance affects a finding.
Datasheet content comes from user values, official web pages, or `notebooklm`
with citations; never open a PDF directly (`rules/engineering.md`). Use
`eng-calc` for a stated, applicable model with identified inputs and assumptions.
Use `design-assist` only when alternatives or design-level trade-offs need to
be explored. Do not load datasheets or invoke companion skills merely by habit.

Use `sch-inspect` when schematic connectivity or circuit intent is
needed to interpret PCB evidence. Do not assume PCB net assignments
alone establish intended electrical behavior.

## Review reasoning

Assess only topics that are relevant to the design and evidence available:

- Placement: functionally related parts, connector access, sensitive-area
  separation, orientation, and manufacturable access.
- Power and return paths: current loops, supply distribution, return-path
  discontinuities, decoupling placement, and local energy storage.
- Routing: layer transitions, widths, routing geometry, reference-plane changes,
  differential or controlled-impedance constraints when specified, and sensitive
  coupling risks.
- Thermal and mechanical: heat sources, copper/thermal paths, component spacing,
  assembly, test, and service considerations.
- Manufacturing: land-pattern evidence, solderability, polarity/orientation,
  tooling, keepouts, and stated fabrication/assembly constraints.

Use native KiCad DRC output and manual visual inspection as separate evidence
sources. Report the exact source, scope, and result of either when available;
their absence is not a pass. DRC does not prove electrical, thermal, EMC, or
manufacturing correctness. Request targeted visual inspection when native data
cannot establish geometry, layer relationships, filled-zone state, or practical
assembly detail.

## Findings and actions

Classify every conclusion clearly:

- **Confirmed defect:** direct CAD, DRC, datasheet, calculation, or visual
  evidence establishes a specific mismatch or violation.
- **Potential risk:** evidence supports a plausible concern but lacks the
  necessary constraint, model, or inspection to confirm it.
- **NOT_VERIFIED:** required evidence is missing, ambiguous, unsupported, or
  outside the tool's scope.

For each material finding, include a severity (`CRITICAL`, `MAJOR`, `MINOR`,
`INFO`, as defined in "Finding format" in `rules/engineering.md`), the status above, the target/location, evidence,
engineering impact, and one practical next check or corrective action. Severity
describes the individual finding, not the board. Recommend changes;
never apply them. Keep the result concise: **Scope**, **Findings**, **Evidence**,
**Limitations / NOT_VERIFIED**, and **Targeted next checks**.

Example finding row:

```text
MAJOR | C14 / U2 VIN | Potential risk | C14 pad centre is 11.8 mm from U2 pin 3 (pad-distance); decoupling effectiveness unproven | pcb-inspect pad-distance, saved board | Higher supply loop inductance | Move C14 closer or confirm with a visual check
```
