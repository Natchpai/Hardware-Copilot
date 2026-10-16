---
name: design-assist
description: >-
  Designs or improves electronic hardware from functional requirements to
  architecture and circuit-level trade-offs. Use when the user asks how to
  design a circuit or subsystem, compare design approaches, choose a topology
  or interface, or review design assumptions before parts are chosen. Not for
  picking a specific part (use component-select).
argument-hint: "[design objective | subsystem | requirements]"
---

# Hardware Design Assistance

Support practical engineering design decisions from first principles, evidence,
and real project constraints. This skill defines **how to approach a design**, not
**which device or topology to use**. The engineer retains final design authority.

## Boundaries

- Do not prescribe a fixed manufacturer, MPN, circuit family, or architecture.
  Consider alternatives that satisfy the actual requirements.
- Treat KiCad designs and libraries as read-only. Never silently change project
  files, selected parts, BOM, review state, or approval records.
- Distinguish known project facts, manufacturer specifications, calculations,
  engineering assumptions, and unverified hypotheses. Mark critical unknowns
  `NOT_VERIFIED`; do not turn assumptions into design requirements.
- Use current manufacturer datasheets, errata, application notes, and relevant
  standards when claims depend on a particular device or revision. Cite the
  source and distinguish recommended operation from absolute maximum ratings.
  Never open or read a PDF directly; use user-supplied values, official web
  pages, or the `notebooklm` skill with its citations (`rules/engineering.md`).
- Do not claim a design is electrically safe, compliant, production-ready, or
  validated solely from reasoning, calculation, or structural inspection.
- Prefer focused evidence over loading full project files, catalogs, or large
  reference documents into context.

## Workflow

1. **Frame the problem.** Establish the intended function, interfaces, input/
   output ranges, operating modes, environmental constraints, performance
   targets, cost, assembly, and user priorities. Identify hard constraints
   versus preferences. Ask only for missing information that changes the design
   materially; otherwise proceed with explicit, bounded assumptions.
2. **Inspect relevant existing context.** For a redesign or ongoing project,
   use targeted schematic evidence and user-provided design information. Do not
   assume an existing circuit is correct or fully understood from partial data.
3. **Generate viable approaches.** Consider appropriate topologies, circuit
   architectures, implementation methods, and trade-offs without locking in
   a specific part. Compare complexity, efficiency, noise, thermal stress,
   control, reliability, manufacturability, and maintenance as applicable.
4. **Analyze operating conditions.** Check nominal and worst-case conditions,
   tolerances, transients, startup/shutdown, abnormal states, protection,
   margins, and relevant interdependencies. Use transparent equations and
   repeatable calculations when needed; show units and assumptions.
5. **Research critical evidence.** Look up device-specific limits, interface
   requirements, reference designs, standards, and practical layout guidance
   when they affect the decision. Prefer authoritative sources; do not invent
   source data or claim online verification without actually obtaining it.
6. **Converge on a proposed design.** Recommend a defensible approach with
   reasons, alternatives rejected, key parameters, implementation risks, and
   the few high-value checks needed next. Avoid endless ideation or arbitrary
   precision.
7. **Separate design from validation.** Propose schematic/PCB inspection,
   simulations, measurements, or review steps as appropriate. Do not mark
   untested behavior `PASS` or imply completed hardware verification.

## Coordination

- Use `component-select` when a functional design needs candidate devices and
  comparative engineering selection; avoid embedding a fixed parts catalog here.
- Use `stock-select` when sourcing, price, quantity, supplier availability, or
  JLCPCB assembly is a constraint. Stock availability is not design suitability.
- Use `component-check` to verify a chosen MPN, package, pin mapping, and
  integration requirements.
- Use `sch-inspect` to obtain targeted native KiCad schematic evidence; its
  connectivity outputs remain scoped and may be `NOT_VERIFIED`.
- Use `eng-calc` for auditable calculations, worst cases and tolerances; if it
  is not installed, calculate transparently with units and assumptions.
- Respect user-directed scope: early design help does not automatically trigger
  a full schematic review, PCB review, purchase, or documentation workflow.

## Output

Provide only what the decision needs:

1. **Requirements & assumptions** : hard constraints, preferences, unknowns.
2. **Design recommendation** : proposed architecture/circuit approach and why.
3. **Engineering basis** : relevant calculations, source-backed limits, and
   meaningful trade-offs; distinguish facts from assumptions.
4. **Risks & next checks** : highest-priority unresolved questions, tests, or
   verification actions. Use `NOT_VERIFIED` for unsupported critical claims.

If multiple approaches remain viable, give a short comparison and a clear
conditional recommendation. If the requirements are mutually inconsistent,
identify the conflict before selecting components.
