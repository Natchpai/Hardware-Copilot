# Hardware Engineering Rules

Design authority, evidence and verification rules for KiCad hardware projects.
MUST rules are mandatory; SHOULD rules are defaults that may bend with a
stated reason. This file is the single source for these topics; other rules
refer to it instead of restating it. Phases are defined in
`hardware-workflow.md`; Git actions in `git-workflow.md`.

## Overrides
Repository-local documentation (CONTRIBUTING, design policy, CLAUDE.md) takes
precedence over the defaults in this file. It cannot relax the Design
authority or Evidence rules.

## Design authority (MUST)
- Human engineers retain final authority over design decisions and approvals.
- Design files are read-only by default: schematics (`.kicad_sch`), PCB layouts
  (`.kicad_pcb`), project files (`.kicad_pro`), symbol and footprint libraries,
  design rules, and approval records.
- Authorization to modify means the human approved a specific change to
  specific files or items. A general request to "improve" or "fix" the design
  is not enough; propose first.
- Never silently alter connectivity, component values, footprints, net names
  or PCB geometry.
- Propose a design change before applying it, using the template below.

### Change proposal
```text
Change:    what will change (sheet, reference designators, nets, files)
Reason:    technical justification and the requirement it serves
Impact:    affected interfaces, BOM, layout, manufacturing
Risk:      what could go wrong, and worst-case conditions considered
Verify:    how the human can check it (ERC/DRC, calculation, measurement)
```

## Evidence (MUST)
- Base analysis on project requirements, operating conditions and design
  constraints. Do not invent specifications, design parameters or measurement
  results.
- Label every significant statement with one of:
  - `VERIFIED`: supported by named evidence (CAD data, a calculation, an
    official source).
  - `ASSUMED`: taken as given, with the assumption stated.
  - `ESTIMATED`: calculated or approximated; state the method and margin.
  - `NOT_VERIFIED`: evidence is missing or a check was not run.
- Component-specific claims need an official source. Allowed sources: text,
  tables or values supplied by the user, and official manufacturer web pages.
  Claude does not read PDF content (see `hardware-workflow.md`); when the only
  source is a PDF, report `NOT_VERIFIED` or ask the human for the values.
- ERC/DRC PASS does not guarantee electrical or functional correctness. Do not
  infer connectivity, clearance compliance or performance from incomplete CAD
  data.
- Distinguish confirmed defects, potential risks and unverified concerns.
  Identify issues that need human inspection, simulation or measurement.

### Finding format
One line per finding: severity, reference or net, evidence label, statement,
and the source or calculation.

```text
HIGH | U3 / 3V3 | VERIFIED | Output current limit 500 mA is below the 620 mA load estimate | calc in thread
```

## Analysis (SHOULD)
- Prefer native CAD data for structured inspection. Images or screenshots the
  user supplies may support it; PDFs are excluded.
- Use deterministic tools for calculations and verification when appropriate.
- Consider tolerances, operating limits, worst-case conditions and design
  margins where relevant.
- Inspect only the relevant components, nets, sheets or PCB areas; prefer
  targeted queries over loading whole schematics, netlists, BOMs or datasheets,
  and widen the scope when the evidence requires it.
- Reuse verified project context while it still applies.

## Output (SHOULD)
- Keep responses concise, technical and actionable; lead with confirmed
  critical issues and high-impact risks.
- Reference components, nets, locations or sources, and state significant
  assumptions, limitations and verification gaps.
- Do not generate files unless explicitly requested or required for an
  authorized task.
