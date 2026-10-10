---
name: component-select
description: >-
  Find and shortlist electronic parts for a hardware design based on requirements,
  operating conditions, availability, and engineering trade-offs. Use when the
  user asks to choose an IC or component, find alternatives, compare functionally
  similar parts, replace an obsolete part, or decide which candidate best fits a
  circuit. Research current manufacturer documentation and sourcing evidence;
  never restrict selection to preset parts, vendors, or circuit topologies.
argument-hint: "[requirements | function | existing MPN]"
---

# Component Selection

Help the engineer reach a defensible selection efficiently. **Search broadly;
recommend narrowly.** This skill defines the selection process, not a catalog
of preferred components. The engineer retains final design authority.

## Boundaries

- Read KiCad design files and libraries without modifying them. Do not change
  BOMs, symbols, footprints, review state, or project configuration.
- Never assume a specific vendor, part family, topology, or package unless the
  design imposes it. Consider already stocked parts when the user prioritizes them.
- Use current manufacturer datasheets, product pages, errata and lifecycle
  notices as primary evidence. Use authorized distributors for stock, lead time,
  and price; clearly identify the region, quantity, date, and uncertainty.
- Distinguish **recommended operating conditions** from absolute maximum
  ratings. Do not use absolute maximum values as normal design targets.
- Do not invent MPNs, orderable suffixes, datasheet figures, prices, stock, or
  pin compatibility. State `NOT_VERIFIED` when critical evidence is unavailable.
- Do not perform an unlimited search or produce an unranked component catalog.

## Workflow

1. **Define the function and constraints.** Extract relevant operating ranges,
   interfaces, electrical stress, temperature, accuracy, noise, speed, package,
   assembly, supply chain, cost, and lifecycle requirements from the request
   and any targeted circuit context. Distinguish hard requirements from
   preferences. Ask only for missing constraints that would materially change
   the decision; otherwise state reasonable assumptions.
2. **Discover candidates.** Search across appropriate manufacturers and, where
   useful, different implementation approaches. Start with parametric search,
   manufacturer technical material, and application notes. Check exact
   **orderable MPN** rather than only a generic family name.
3. **Apply hard filters first.** Reject candidates that fail mandatory functional,
   electrical, environmental, interface, package, or lifecycle constraints.
   Flag missing critical specifications as `NOT_VERIFIED`, not PASS. Avoid
   selecting on a weighted score before hard constraints are checked.
4. **Compare survivors.** Evaluate relevant performance at the actual operating
   conditions, tolerances and derating, external circuitry, board area, PCB
   complexity, thermal limits, documentation, availability, sourcing risk,
   cost at the user's quantities, and migration effort. Apply calculations
   when useful and identify assumptions and worst cases.
5. **Check integration risks.** Look for suffix/package differences, pin functions,
   exposed-pad requirements, startup behavior, sequencing, protection, stability,
   layout requirements, and errata relevant to the design. When the user already
   has a part, distinguish a functional alternative from a pin-compatible or
   drop-in replacement; never imply interchangeability without evidence.
6. **Recommend a shortlist.** Aim for 2–3 meaningful choices: best overall fit,
   a defensible alternative, and (when relevant) a cost/availability option.
   Explain why the recommended device wins, what it sacrifices, and what could
   change the decision. Give a clear conclusion rather than a long list.
7. **Stop searching when justified.** Stop once hard constraints are met,
   important trade-offs are distinguishable, major integration risks are checked,
   and an adequate alternative exists. Continue only if evidence is weak or a
   materially better candidate is plausible.

## Coordination

- Use `component-check` for deep verification of selected MPNs, symbol/pinout,
  footprint/package, BOM consistency, or substitution compatibility.
- Use `sch-inspect` for targeted as-designed schematic evidence when needed.
- Use supported calculations or trusted engineering references to check sizing,
  stress, thermal, and tolerance claims. Do not claim that a separate calculator
  skill or PCB parser exists until available.
- Retrieve only the documentation sections needed for the current decision;
  do not ingest full catalogs or entire KiCad projects by default.

## Output

Report concisely:

1. **Decision context:** function, hard constraints, preferences, assumptions.
2. **Shortlist:** exact manufacturer/MPN, differentiating parameters, material
   trade-offs, and evidence links or datasheet sections.
3. **Disposition:** `RECOMMENDED`, `ALTERNATIVE`, `REJECTED`, or `NOT_VERIFIED`
   with the specific reason; make uncertainty visible per critical claim.
4. **Next verification:** only the most important unresolved datasheet,
   electrical, footprint, thermal, or sourcing checks before design commitment.

If no candidate passes hard constraints, say so and propose which constraint or
architecture might need revision. Never label an unverified part as approved.
