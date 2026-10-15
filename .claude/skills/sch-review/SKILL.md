---
name: sch-review
description: >-
  Review an electronic schematic or a focused circuit block for engineering
  correctness, risks, missing protections, component suitability, and design
  assumptions. Use when the user asks for a schematic review, circuit design
  check, power or signal-path review, or assessment of a KiCad schematic before
  PCB layout. Coordinate targeted schematic evidence, calculations, and
  datasheets; do not mistake inspection for design verification.
argument-hint: "[sheet | subsystem | reference | concern]"
---

# Schematic Engineering Review

Review the **engineering design**, not just the syntactic structure of a
schematic. Select checks based on the circuit's purpose and constraints rather
than a fixed topology, manufacturer, or checklist of specific devices. The
engineer makes final design and release decisions.

## Boundaries

- Treat KiCad schematic, project, library, BOM, and review records as read-only.
  Do not change symbols, connectivity, review status, approvals, or project files.
- Remain independent of any separate formal Hardware Review Framework, gate,
  checklist state, or release workflow. Do not invent PASS/closure decisions for
  an entire project from a targeted review.
- Prefer bounded queries of the requested block or concern. Do not dump full
  schematic files into context or export a full netlist by default.
- Separate **observed schematic evidence**, **calculated results**,
  **datasheet requirements**, **engineering inferences**, and **unknowns**.
  Unsupported or ambiguous connections must be marked `NOT_VERIFIED`.
- Never infer electrical correctness merely from matching net labels, a parser's
  proposed connection, ERC success, or absence of visible errors.
- Do not invent ratings, component values, design requirements, or sources.
  Check part-specific claims against the actual MPN and current documentation
  (never open a PDF directly; use user values, official web pages, or
  `notebooklm` with citations, per `rules/engineering.md`).
- No automatic changes, purchasing, commit, reports, or persistent logs unless
  explicitly requested and allowed by repository rules.

## Workflow

1. **Scope the review.** Identify the intended function, requested circuit
   block, known operating range and review objective. Prefer the user's specific
   concern over a project-wide sweep. Ask for a critical missing constraint only
   if proceeding would be misleading; otherwise declare assumptions.
2. **Collect targeted evidence.** Use `sch-inspect` for relevant symbols, pins,
   local/hierarchical/project connectivity and instance paths. Identify the
   actual scope and unresolved parser semantics. Request a human visual check
   for cases that cannot be established from native data.
3. **Reconstruct intended behavior.** Establish the signal/power path, operating
   modes, startup/shutdown, interfaces, expected loading, and fault scenarios
   relevant to the block. Do not assume the circuit works because it is wired.
4. **Choose risk-based checks.** Evaluate applicable items such as operating
   limits, component stress, power paths, decoupling, biasing, pull-ups/downs,
   floating pins, protection, feedback stability, timing, signal integrity,
   grounding, sequencing, and interface compatibility. Skip irrelevant items;
   do not claim they were checked.
5. **Validate calculations and components.** Use `eng-calc` for quantitative
   stress, tolerance, thermal, timing, or worst-case checks; `component-check`
   for actual pin mapping, MPN, package and datasheet requirements. Use
   `component-select` or `stock-select` only when alternatives or sourcing are
   requested or materially necessary to resolve a finding.
6. **Challenge assumptions.** Inspect at least one meaningful adverse condition
   when applicable (e.g., input extremes, transient, reverse current, reset,
   unpowered interface, startup, short circuit). Distinguish a demonstrated
   defect from a plausible risk requiring further evidence.
7. **Report and stop.** Prioritize actionable findings and targeted next checks.
   Do not expand scope indefinitely. If required evidence is unavailable,
   report the boundary rather than supplying a fictional verification result.

## Findings and severity

- `CRITICAL`: credible hazard or design defect with potentially severe impact,
  supported by clear evidence; describe the conditions, not absolute certainty.
- `MAJOR`: likely functional or reliability issue that requires design attention.
- `MINOR`: bounded improvement, margin concern, or documentation issue.
- `INFO`: observation or optional suggestion, not an identified defect.
- `NOT_VERIFIED`: insufficient or unsupported evidence to determine correctness;
  **not** equivalent to PASS or FAIL.

Severity describes impact and evidence for the *individual finding*, not the
status of the whole schematic. Identify uncertainties explicitly; avoid
inflating hypothetical worst cases into proven faults.

## Coordination and scope limits

- `sch-inspect` supplies scoped structural evidence; its `project-net` results
  are not guaranteed full KiCad netlist/ERC parity. Respect its bus, inherited
  symbol, hidden-connectivity, and ambiguous-instance limitations.
- `eng-calc` supports auditable equations, units, tolerances, and worst cases.
- `component-check` verifies selected device datasheets and physical mappings.
- `design-assist` supports architectural alternatives when the review reveals
  a fundamental design-choice question.
- ERC, simulations, laboratory measurements, PCB checks, and formal release
  processes are separate activities. Recommend them where needed but never
  imply they were performed.

## Output

Keep output proportional to the requested review. For a substantive review:

1. **Target & scope** : block/sheet, operating assumptions, evidence reviewed.
2. **Findings** : compact table with severity, reference/pin/net, issue,
   supporting evidence, impact, and recommended action; distinguish confirmed
   defects from potential risks.
3. **NOT_VERIFIED** : missing requirements, ambiguous connectivity, unverified
   datasheet data, or untested behavior.
4. **Next checks** : a small prioritized set of human visual checks,
   calculations, simulations, ERC, or measurements necessary to close uncertainty.

Example finding row:

```text
MAJOR | U3 pin 4 / EN | Potential risk | EN is tied to VIN through R12 only; no divider for UVLO | sch-inspect local-net, datasheet table 6 (via NotebookLM) | Startup below the intended input voltage | Add a divider or confirm the intended threshold
```

If no supported issue is found, say **"No issue found within the inspected
scope"**, not "schematic verified" or "ready for fabrication".
