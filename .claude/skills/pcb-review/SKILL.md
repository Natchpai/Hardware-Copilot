---
name: pcb-review
description: >-
  Reviews a KiCad PCB layout, read-only and evidence-based. Use when the user
  asks to assess layout risks, placement, routing, power, thermal,
  signal-integrity or manufacturability concerns in a PCB design. Not for
  looking up layout data only (use pcb-inspect).
argument-hint: "[board, area, net, reference, or review concern]"
---

# PCB Layout Review

Review the requested scope as an engineering assessment, not an approval or a
design-state change. Native KiCad files are the source of truth. PCB, library,
project and review files stay unchanged.

## Scope and evidence

Start from the project's requirements, operating conditions, constraints and
the user's review question. Pick the smallest useful focus: a board area,
power domain, interface, component group, net or manufacturing risk. Choose
checks from the design itself, not from a fixed circuit-type checklist or an
architecture guessed from reference designators or net names.

Use `pcb-inspect` for targeted saved-board evidence:

- `summary`, `footprint` and `nearby` for placement context.
- `pads` and `pad-distance` for transformed pad-centre geometry and assignments.
- `net` for saved pad assignments only.
- `tracks` and `vias` for saved routing primitive geometry and metadata.

Respect its bounded output, ambiguity results and `NOT_VERIFIED` states. A
shared net name, track assignment, via assignment or geometric distance does
not prove copper continuity, clearance, route completeness, return-path quality
or electrical behavior.

Results reflect the saved `.kicad_pcb` file, not unsaved edits in the KiCad PCB
Editor. Report editor-state consistency as `NOT_VERIFIED` unless it was
checked.

Use `component-check` and the datasheet only when the exact part, package,
rating, pinout, thermal or layout guidance changes a finding. Datasheet values
follow "Datasheet evidence" in `rules/engineering.md`: user values, official
web pages, or `notebooklm` with citations. Use `eng-calc` for a stated model
with known inputs and assumptions, and `design-assist` only when alternatives
or design-level trade-offs need exploring. Call a companion skill only when the
finding needs it.

Use `sch-inspect` when schematic connectivity or circuit intent is needed to
read the PCB evidence. PCB net assignments alone do not show the intended
electrical behavior.

## Review reasoning

Assess only the topics that apply to the design and the evidence you have:

- Placement: related parts together, connector access, separation of sensitive
  areas, orientation, and access for assembly.
- Power and return paths: current loops, supply distribution, return-path
  breaks, decoupling placement and local energy storage.
- Routing: layer changes, widths, routing geometry, reference-plane changes,
  differential or controlled-impedance constraints when specified, and
  coupling into sensitive nets.
- Thermal and mechanical: heat sources, copper and thermal paths, component
  spacing, assembly, test and service.
- Manufacturing: land-pattern evidence, solderability, polarity and
  orientation, tooling, keepouts, and stated fabrication or assembly limits.

Native KiCad DRC output and manual visual inspection are separate evidence
sources. When either is available, report its exact source, scope and result;
a missing DRC or visual check is not a pass. DRC does not prove electrical,
thermal, EMC or manufacturing correctness. Ask for a targeted visual check
when native data cannot settle geometry, layer relationships, filled-zone
state or assembly detail.

## Findings and actions

Give every conclusion a status:

- **Confirmed defect:** direct CAD, DRC, datasheet, calculation or visual
  evidence shows a specific mismatch or violation.
- **Potential risk:** the evidence supports a plausible concern but lacks the
  constraint, model or inspection to confirm it.
- **NOT_VERIFIED:** the needed evidence is missing, ambiguous, unsupported or
  outside the tool's scope.

For each finding give: severity (`CRITICAL`, `MAJOR`, `MINOR` or `INFO`, as
defined in "Finding format" in `rules/engineering.md`), the status above, the
evidence label, target and location, evidence source, engineering impact, and
one next check or corrective action. Severity rates the individual finding,
not the board. Recommend changes; never apply them. Output sections:
**Scope**, **Findings**, **Evidence**, **Limitations / NOT_VERIFIED** and
**Targeted next checks**.

Example finding row:

```text
MAJOR | C14 / U2 VIN | Potential risk | VERIFIED | C14 pad centre is 11.8 mm from U2 pin 3 (pad-distance); decoupling effectiveness unproven | pcb-inspect pad-distance, saved board | Higher supply loop inductance | Move C14 closer or confirm with a visual check
```
