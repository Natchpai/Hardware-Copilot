---
name: sch-review
description: >-
  Reviews an electronic schematic or a focused circuit block for engineering
  correctness, risks, missing protection, component suitability and design
  assumptions. Use when the user asks for a schematic review, a circuit design
  check, a power or signal-path review, or an assessment of a KiCad schematic
  before PCB layout. Not for looking up schematic data only (use sch-inspect).
argument-hint: "[sheet | subsystem | reference | concern]"
---

# Schematic Engineering Review

Review the **engineering design**, not just the schematic's structure. Pick the
checks from the circuit's purpose and constraints, not from a fixed topology,
manufacturer or device checklist.

## Boundaries

- KiCad schematic, project, library, BOM and review records are read-only.
  Recommend changes to symbols, connectivity, review status or approvals; do
  not apply them.
- A targeted review rates the inspected scope only. It is not a project-wide
  PASS, a gate closure, or part of a formal review framework.
- Query the requested block or concern only. Use targeted queries, not full
  schematic dumps or a full netlist export.
- Label each claim `VERIFIED`, `ASSUMED`, `ESTIMATED` or `NOT_VERIFIED`
  (`rules/engineering.md`). Keep schematic evidence, calculations, datasheet
  requirements, inferences and unknowns apart. An unsupported or ambiguous
  connection is `NOT_VERIFIED`.
- Matching net labels, a parser's proposed connection, ERC success, or no
  visible errors do not show electrical correctness.
- Check part-specific claims against the actual MPN and current documentation.
  Datasheet values follow "Datasheet evidence" in `rules/engineering.md`: user
  values, official web pages, or `notebooklm` with citations.
- Changes, purchases, commits, reports and logs happen only when the user asks
  and the repository rules allow them.

## Workflow

1. **Scope the review.** The block's intended function, its known operating
   range, and the review goal. Prefer the user's specific concern over a
   project-wide sweep. Ask for a missing constraint only if going on without it
   would mislead; otherwise state the assumption.
2. **Collect targeted evidence.** Use `sch-inspect` for the relevant symbols,
   pins, local, hierarchical and project connectivity, and instance paths.
   Record the scope it actually covered and any parser limits. Ask for a human
   visual check where native data cannot settle a question.
3. **Rebuild the intended behavior.** Signal and power path, operating modes,
   startup and shutdown, interfaces, expected loading and fault cases for the
   block. Being wired is not the same as working.
4. **Choose risk-based checks.** Operating limits, component stress, power
   paths, decoupling, biasing, pull-ups and pull-downs, floating pins,
   protection, feedback stability, timing, signal integrity, grounding,
   sequencing and interface compatibility, as they apply. Report only the
   checks you actually ran.
5. **Check calculations and components.** `eng-calc` for stress, tolerance,
   thermal, timing or worst-case numbers; `component-check` for pin mapping,
   MPN, package and datasheet requirements. Use `component-select` or
   `stock-select` only when the user asks for alternatives or sourcing, or a
   finding cannot be resolved without them.
6. **Challenge assumptions.** Test at least one adverse condition where it
   applies: input extremes, transients, reverse current, reset, an unpowered
   interface, startup or a short circuit. Keep a demonstrated defect apart
   from a plausible risk that needs more evidence.
7. **Report and stop.** Lead with actionable findings and targeted next checks.
   Stop at the requested scope. Where evidence is missing, report the gap
   instead of a verification result.

## Findings

Give each finding a severity and a status:

- **Severity:** `CRITICAL`, `MAJOR`, `MINOR` or `INFO`, as defined in "Finding
  format" in `rules/engineering.md`. Severity rates the individual finding,
  not the whole schematic.
- **Status:** **Confirmed defect** (direct CAD, datasheet or calculation
  evidence shows a specific mismatch), **Potential risk** (a plausible concern
  that lacks the constraint, model or inspection to confirm it), or
  `NOT_VERIFIED` (the evidence is not enough to decide; **not** a PASS or
  FAIL).

State uncertainties plainly, and keep hypothetical worst cases as risks, not
proven faults.

## Coordination and scope limits

- `sch-inspect` gives scoped structural evidence. Its `project-net` results are
  not full KiCad netlist or ERC parity. Respect its limits on buses, inherited
  symbols, hidden connectivity and ambiguous instances.
- `eng-calc`: auditable equations, units, tolerances and worst cases.
- `component-check`: datasheet and physical mapping of a chosen device.
- `design-assist`: architecture alternatives when the review raises a basic
  design-choice question.
- ERC, simulation, lab measurement, PCB checks and formal release are separate
  activities. Recommend them where needed and say they were not performed.

## Output

Match the size of the output to the requested review. For a full review:

1. **Target and scope:** block or sheet, operating assumptions, evidence
   reviewed.
2. **Findings:** one row per finding, with severity, reference/pin/net,
   status, evidence label, issue, evidence source, impact and recommended
   action.
3. **NOT_VERIFIED:** missing requirements, ambiguous connectivity, unchecked
   datasheet data, or untested behavior.
4. **Next checks:** a short, ordered list of the visual checks, calculations,
   simulations, ERC runs or measurements that would close the gaps.

Example finding row:

```text
MAJOR | U3 pin 4 / EN | Potential risk | VERIFIED | EN is tied to VIN through R12 only; no divider for UVLO | sch-inspect local-net, datasheet table 6 (via NotebookLM) | Startup below the intended input voltage | Add a divider or confirm the intended threshold
```

If no supported issue is found, say **"No issue found within the inspected
scope"**, not "schematic verified" or "ready for fabrication".
